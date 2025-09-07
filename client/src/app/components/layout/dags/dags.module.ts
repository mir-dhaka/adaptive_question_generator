import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { DagsRoutingModule } from './dags-routing.module'; 

// Import the standalone component
import { ListComponent } from '../../primeng/components/list/list';
import { AccordionComponent } from '../../primeng/components/list/accordion';
import { CalendarComponent } from '../../primeng/components/embeddable/calendar.component';

@NgModule({
    declarations: [],
    imports: [CommonModule, DagsRoutingModule, ListComponent, AccordionComponent, CalendarComponent]
})
export class DagsModule {}
