import { Component } from '@angular/core';
import { ImportsModule } from '../../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../../services/data.service';
import { environment } from '../../../../../../environments/environment';

@Component({
    selector: 'pn-calculatedmastery',
    templateUrl: './calculatedmastery.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class CalculatedMasteryComponent {
    private _slug: string;
    public get slug(): string {
        return this._slug;
    }
    public set slug(value: string) {
        this._slug = value;
    }
    itemName: string; 
    items: any[] = [];
    item: any;  

    constructor(
        private messageService: MessageService, 
        private service: DataService
    ) { }
    ngOnInit() {
        this.slug = 'get-mastery-report';
        this.itemName = 'Calculated Mastery';
        setTimeout(() => {
            this.loadItems(true);
        }, 100);
    }
    loadItems(showToast: boolean = false) {
        this.service.process(this.slug,{}, (res) => { 
            if (res.body.success == true) {
                this.items = res.body.data;
                if (showToast) {
                    this.showSuccessToast(`${this.itemName} loead successfully`);
                }
            } else {
                this.items = [];
                this.showErrorToast(`Failed to load ${this.itemName}`, 'Load Data');
            }
        });
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
