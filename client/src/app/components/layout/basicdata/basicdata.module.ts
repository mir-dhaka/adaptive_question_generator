import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { BasicDataRoutingModule } from './basicdata-routing.module';
import { BasicDataComponent } from './basicdata.component';

// Import the standalone component
import { ListComponent } from '../../primeng/components/list/list';
import { AccordionComponent } from '../../primeng/components/list/accordion';
import { CalendarComponent } from '../../primeng/components/embeddable/calendar.component';

@NgModule({
    declarations: [BasicDataComponent],
    imports: [CommonModule, BasicDataRoutingModule, ListComponent, AccordionComponent, CalendarComponent]
})
export class BasicDataModule {}
