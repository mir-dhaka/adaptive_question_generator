import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ActivatedRoute } from '@angular/router';
import { DataService } from '../../../../services/data.service';
import { ConfirmationService, MessageService } from 'primeng/api';

@Component({
    selector: 'pn-calendar',
    standalone: true,
    imports: [ImportsModule],
    template: `<div class="card flex justify-content-center">
            <p-calendar
                [(ngModel)]="rangeDates"
                selectionMode="range"
                [readonlyInput]="true"
                dateFormat="mm/dd/yy"
                (onSelect)="onDateSelect()"
            >
            </p-calendar>
        </div>
        <p *ngIf="formattedRange">{{ formattedRange }}</p>
        <button (click)="onSave()">Save</button>
        <button (click)="onLoad()">Load</button>
        <select (change)="onDropdownChange($event.target.value)">
            <option *ngFor="let item of dropdownItems" [value]="item">{{ item }}</option>
        </select> `
})
export class CalendarComponent {
    @Input() rangeDates: Date[];
    @Input() dropdownItems: string[];
    @Input() onExternalMethod: (value: any) => void;
    @Output() save = new EventEmitter<void>();
    @Output() load = new EventEmitter<void>();

    formattedRange: string;

    constructor(
        private route: ActivatedRoute,
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) {}

    onDateSelect() {
        this.formatDateRange();
        this.onExternalMethod?.(this.rangeDates);
    }

    onSave() {
        this.save.emit();
    }

    onLoad() {
        this.load.emit();
    }

    formatDateRange() {
        if (this.rangeDates && this.rangeDates.length === 2) {
            const startDate = this.formatDate(this.rangeDates[0]);
            const endDate = this.formatDate(this.rangeDates[1]);
            this.formattedRange = `${startDate} - ${endDate}`;
        } else {
            this.formattedRange = '';
        }
    }

    formatDate(date: Date): string {
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based
        const year = date.getFullYear();
        return `${month}/${day}/${year}`;
    }

    onDropdownChange(selectedValue: string) {
        this.onExternalMethod?.(selectedValue);
    }

    // Method to be called from parent
    setRangeDates(startDate: Date, endDate: Date) {
        this.rangeDates = [startDate, endDate];
        this.formatDateRange();
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
