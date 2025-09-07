import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { HarvestingRoutingModule } from './harvesting-routing.module';

// Import the standalone component
import { ListComponent } from '../../primeng/components/list/list';
import { AccordionComponent } from '../../primeng/components/list/accordion';
import { CalendarComponent } from '../../primeng/components/embeddable/calendar.component';
import { HarvestingComponent } from './harvesting.component';

@NgModule({
    declarations: [HarvestingComponent],
    imports: [CommonModule, HarvestingRoutingModule, ListComponent, AccordionComponent, CalendarComponent]
})
export class HarvestingModule { }
