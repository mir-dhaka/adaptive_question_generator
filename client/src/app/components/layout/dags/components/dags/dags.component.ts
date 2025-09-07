import { Component } from '@angular/core';
import { ImportsModule } from '../../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../../services/data.service';
import { environment } from '../../../../../../environments/environment';

@Component({
    selector: 'pn-dags',
    templateUrl: './dags.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class DagsComponent {
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

    // dag dialog
    showDagDialog: boolean = false;
    dagImageUrl: string = "";
    dagView:string="DAG View"

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }
    ngOnInit() {
        this.slug = 'dags';
        this.itemName = 'DAG';
        setTimeout(() => {
            this.loadItems(true);
        }, 100);
    }
    loadItems(showToast: boolean = false) {
        this.service.getAll('dags', (res) => {
            if (res.success == true) {
                this.items = res.data;
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
        this.submitted = true;
        this.service.upsert(this.slug, this.item, (res) => {
            if (res.success == true) {
                this.showSuccessToast(`${this.itemName} saved`);
                this.loadItems();
                this.hideDialog();
            } else {
                this.showErrorToast(`Failed to save ${this.item.title}`, `Save`);
            }
        });
    }
    deleteSelectedItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }
    deleteItem(item: any) {
        const name = `${item.title}`;
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

    openDagDialog(item: any) {
        this.dagView=`DAG: ${item.title}`;
        const payload = { id: item.id };
        this.service.process('get-dag-url', payload, (res) => {
            if (res.body.success == true) {
                this.dagImageUrl = `${environment.apiHost}/files/${res.body.data.file_name}`;
                this.showDagDialog = true;
                debugger;
            } else {
                this.dagImageUrl = '';
                this.showDagDialog = false;
            }
        });

    }

    openNew() {
        this.item = {};
        this.submitted = false;
        this.itemDialog = true;
    }
    editItem(item: any) {
        this.item = { ...item };
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
