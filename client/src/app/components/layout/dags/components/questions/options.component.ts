import { Component } from '@angular/core';
import { ImportsModule } from '../../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../../services/data.service';

@Component({
    selector: 'pn-options',
    templateUrl: './options.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class OptionsComponent {
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
    questionList: any[] = [];
    selectedQuestion: any;
    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }
    ngOnInit() {
        this.slug = 'options';
        this.itemName = 'Options';
        this.getQuestionList();
    }
    getQuestionList() {
        this.service.getAll('questions', (res) => {
            if (res.success == true) {
                this.questionList = res.data;
                setTimeout(() => {
                    this.loadItems(true);
                }, 100);
            } else {
                this.questionList = [];
            }
        });
    }

    loadItems(showToast: boolean = false) {
        this.service.getAll(this.slug, (res) => {
            if (res.success == true) {
                this.items = res.data.map((item: any) => { 
                    const q = this.questionList.find(x => x.id === item.question_id);
                    return {
                        ...item,
                        question: q?.title || null // attach kc object, or null if not found
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
        this.submitted = true;
        this.item['question_id'] = this.selectedQuestion;
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
        const name = `Option`;
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
        this.selectedQuestion=null;
    }
    editItem(item: any) {
        this.item = { ...item };
        this.selectedQuestion=item.question_id;
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
