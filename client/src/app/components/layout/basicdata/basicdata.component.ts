import { Component, OnInit, ViewChild } from '@angular/core';
import { CalendarComponent } from '../../primeng/components/embeddable/calendar.component';

@Component({
    selector: 'basic-data',
    templateUrl: './basicdata.component.html'
})
export class BasicDataComponent implements OnInit {
    @ViewChild('calendarComp') calendarComponent: CalendarComponent;
    constructor() {}

    ngOnInit() {}

    rangeDates: Date[];
    dropdownItems: string[] = ['Option 1', 'Option 2', 'Option 3'];

    ngAfterViewInit() {
        // You can now call child component methods here if needed
    }

    handleSave() {
        console.log('Save event triggered');
    }

    handleLoad() {
        console.log('Load event triggered');
    }

    handleExternalMethod(value: any) {
        console.log('External method called with value:', value);
    }

    setDates() {
        const startDate = new Date(2023, 0, 1); // January 1, 2023
        const endDate = new Date(2023, 11, 31); // December 31, 2023
        this.calendarComponent.setRangeDates(startDate, endDate);
    }
}
