import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { SyntheticDataRoutingModule } from './syntheticdata-routing.module';

// Import the standalone component
import { ListComponent } from '../../primeng/components/list/list';
import { AccordionComponent } from '../../primeng/components/list/accordion';
import { CalendarComponent } from '../../primeng/components/embeddable/calendar.component';

@NgModule({
    declarations: [],
    imports: [CommonModule, SyntheticDataRoutingModule, ListComponent, AccordionComponent, CalendarComponent]
})
export class SyntheticDataModule {}
