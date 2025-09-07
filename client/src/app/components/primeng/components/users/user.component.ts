import { Component } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../services/data.service';

@Component({
    selector: 'pn-users',
    templateUrl: './users.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class UsersComponent {
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
    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) {}
    ngOnInit() {
        this.slug = 'users';
        this.itemName = 'users';
        setTimeout(() => {
            this.loadItems(true);
        }, 100);
    }
    loadItems(showToast: boolean = false) {
        this.service.ddata('users_ddata', { x: 1 }, (res) => {
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
        this.service.create(this.slug, this.item, (res) => {
            if (res.success == true) {
                this.showSuccessToast(`${this.itemName} saved`);
                this.loadItems();
                this.hideDialog();
            } else {
                const name = `${this.item.firstName} ${this.item.lastName}`;
                this.showErrorToast(`Failed to save ${name}`, `Save`);
            }
        });
    }
    deleteSelectedItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }
    deleteItem(item: any) {
        const name = `${item.firstName} ${item.lastName}`;
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
