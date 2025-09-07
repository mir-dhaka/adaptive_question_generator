import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../services/data.service';

@Component({
    selector: 'pn-crud',
    templateUrl: './crud.html',
    standalone: true,
    imports: [ImportsModule]
})
export class CRUDComponent {
    @Input() inputData: CRUDComponentInputModel;
    @Input() onExternalMethod: (value: any) => void; //general data handler
    @Output() save = new EventEmitter<any>(); // save handler
    @Output() load = new EventEmitter<any>(); //load-data handler
    @Output() delete = new EventEmitter<any>(); //load-data handler
    @Output() deleteSelected = new EventEmitter<any>(); //load-data handler
    @Output() export = new EventEmitter<any>(); //load-data handler
    @Output() import = new EventEmitter<any>(); //load-data handler

    //crud objects
    itemName: string;
    slug: string;
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

    onLoad() {
        this.load.emit(this.inputData.filterObj);
    }

    loadItems(items: any[]) {
        this.items = items;
    }

    onSave() {
        this.save.emit(this.item);
    }
    onDelete() {
        this.delete.emit(this.item);
    }
    onDeleteSelected() {
        this.deleteSelected.emit(this.selectedItems);
    }
    onImport() {
        this.import.emit(null);
    }
    onExport() {
        this.import.emit(null);
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

export interface CRUDComponentInputModel {
    filterObj: CRUDFilterObject;
    listObj: CRUDListObject;
    formObj: CRUDFormObject;
}
export interface CRUDFilterObject {
    title: string;
    filters: CRUDFilter[];
    loadButtonText: string;
    filterCriteria: string;
}
export interface CRUDFilter {
    name: string;
    displayText: string;
    controlType: string;
    displayOrder: number;
    selctedValue: any;
    selectedValues: any[];
    dataSource: any[];
    dependsOn: string[]; //name of filters this depends on.
    modifies: string[]; // name of filters affected by this.
}
export interface CRUDListObject {
    title: string;
    columns: CRUDListColumn[];
}
export interface CRUDListColumn {
    name: string;
    displayText: string;
    datatype: string;
    displayOrder: number;
    hidden: boolean;
    render: (rowItem: any) => {};
}
export interface CRUDFormObject {}
export interface CRUDFormRow {}
