import { Component } from '@angular/core';
import { ImportsModule } from '../../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../../services/data.service';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Component({
    selector: 'pn-dagedges',
    templateUrl: './dagedges.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class DagedgesComponent {
    private _slug: string;
    public get slug(): string {
        return this._slug;
    }
    public set slug(value: string) {
        this._slug = value;
    }
    itemName: string;
    itemDialog: boolean;
    items: any[] = [];
    item: any;
    selectedItems: any[] = [];
    submitted: boolean;

    // ref items 
    dagList: any[] = [];
    kcList: any[] = [];

    selectedDag: any;
    selectedFromKc: any;
    selectedToKc: any;

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }
    ngOnInit() {
        this.slug = 'dag_edges';
        this.itemName = 'DAG Edge';

        forkJoin({
            dags: this.service._getAll('dags').pipe(
                catchError(err => {
                    console.error('Error loading dags', err);
                    return of(this.service._getErrorResponse());
                })
            ),
            kcs: this.service._getAll('kcs').pipe(
                catchError(err => {
                    console.error('Error loading kcs', err);
                    return of(this.service._getErrorResponse());
                })
            )
        }).subscribe(({ dags, kcs }: any) => {
            this.dagList = dags.success ? dags.data : [];
            this.kcList = kcs.success ? kcs.data : [];
            this.loadItems(); // safe now, both lists are loaded
        });
    } 

    loadItems(showToast: boolean = false) {
        this.service.getAll(this.slug, (res) => {
            if (res.success == true) {
                this.items = res.data.map((q: any) => {
                    const dag = this.dagList.find(k => k.id === q.dag_id);
                    const from_kc = this.kcList.find(k => k.id === q.from_kc_id);
                    const to_kc = this.kcList.find(k => k.id === q.to_kc_id);
                    return {
                        ...q,
                        dag: dag?.title || null,
                        from: from_kc?.title || null,
                        to: to_kc?.title || null
                    };
                });
                if (showToast) {
                    this.showSuccessToast(`${this.itemName} loead successfully`);
                }
            } else {
                this.items = [];
                this.showErrorToast(`Failed to load ${this.itemName}`, 'Load Data');
            }
        });
    }

    saveItem() {
        //https://cytoscape.org/cytoscape.js-dagre/
        this.submitted = true; 
        this.item.dag_id=this.selectedDag;
        this.item.from_kc_id=this.selectedFromKc;
        this.item.to_kc_id=this.selectedToKc;
        this.service.upsert(this.slug, this.item, (res) => {
            if (res.success == true) {
                this.showSuccessToast(`${this.itemName} saved`);
                this.loadItems();
                //this.hideDialog();
            } else {
                this.showErrorToast(`Failed to save Edge`, `Save`);
            }
        });
    }
    deleteSelectedItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }
    deleteItem(item: any) {
        const name = `DAG Edge`;
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete ' + name + '?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.submitted = true;
                this.service.delete(this.slug, item.id, (res) => {
                    if (res.success == true) {
                        this.showSuccessToast(`${name} Deleted`, 'Delete');
                        this.loadItems();
                    } else {
                        this.showErrorToast(`Failed to delete ${name}`, 'Delete');
                    }
                });
            }
        });
    }

    importItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    exportItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    openNew() {
        this.item = {};
        this.submitted = false;
        this.itemDialog = true;
        this.selectedDag = null;
        this.selectedFromKc = null;
        this.selectedToKc = null;
    }
    editItem(item: any) {
        this.item = { ...item };
        this.selectedDag = item.dag_id;
        this.selectedFromKc = item.from_kc_id;
        this.selectedToKc = item.to_kc_id;
        this.itemDialog = true;
    }
    hideDialog() {
        this.itemDialog = false;
        this.submitted = false;
    }
    showSuccessToast(message: string, title: string = 'Success'): void {
        this.messageService.add({
            severity: 'success',
            summary: title,
            detail: message,
            life: 3000
        });
    }
    showInfoToast(message: string, title: string = 'Info'): void {
        this.messageService.add({
            severity: 'info',
            summary: title,
            detail: message,
            life: 3000
        });
    }
    showErrorToast(message: string, title: string = 'Failed'): void {
        this.messageService.add({
            severity: 'error',
            summary: title,
            detail: message,
            life: 3000
        });
    }
}
