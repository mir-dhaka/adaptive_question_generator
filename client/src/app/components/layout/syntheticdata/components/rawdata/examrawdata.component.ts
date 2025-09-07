import { Component } from '@angular/core';
import { ImportsModule } from '../../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../../services/data.service';

@Component({
    selector: 'pn-examrawdata',
    templateUrl: './examrawdata.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class ExamRawDataComponent {
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

    //create profile
    createProfileDialog: boolean = false
    dagList: any[] = []
    selectedDag: any

    //check-data
    checkDataDialog: boolean = false;
    checkDataList: any[] = [];



    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }
    ngOnInit() {
        this.slug = 'simulated_exam_data_raw';
        this.itemName = 'Exam Raw Data';
        this.loadItems(true);
    } 

    loadItems(showToast: boolean = false) {
        this.service.getAll(this.slug, (res) => {
            if (res.success == true) {
                this.selectedItems = [];
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
            const name = `this ${this.itemName}`;
            if (res.success == true) {
                this.showSuccessToast(`${this.itemName} saved`);
                this.loadItems();
                this.hideDialog();
            } else {
                this.showErrorToast(`Failed to save ${this.itemName}`, `Save`);
            }
        });
    }

    createProfileForSelectedItems() {
        this.service.process('create-exam-profiles', this.selectedItems, (res) => {
            if (res.body.success == true) { 
                const msg=`${res.body.data.length} masteries created successfully`;
                this.showSuccessToast(msg, 'Info');
                this.loadItems();
            } else {
                this.showErrorToast(`Failed to create masteries`, 'Info');
            }
        });
    }

    checkProfileData() {
        this.checkDataList = [];
        this.service.process('check-exam-data-validity', this.selectedItems, (res) => {
            if (res.body.success == true) {
                this.checkDataList = res.body.data;
                this.showSuccessToast(`Data checked successfully`, 'Info');
            } else {
                this.showErrorToast(`Failed to check data`, 'Info');
            }
        });
        this.checkDataDialog = true;
    }


    deleteSelectedItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    deleteItem(item: any) {
        const name = `this ${this.itemName}`;
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
