import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { BlankPageRoutingModule } from './blank-page-routing.module';
import { BlankPageComponent } from './blank-page.component';

// Import the standalone component
import { ListComponent } from '../../primeng/components/list/list';
import { AccordionComponent } from '../../primeng/components/list/accordion';

@NgModule({
    imports: [CommonModule, BlankPageRoutingModule, ListComponent, AccordionComponent],
    declarations: [BlankPageComponent]
})
export class BlankPageModule {}
