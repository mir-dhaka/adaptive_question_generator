import { Component } from '@angular/core';
import { ImportsModule } from '../../imports';
@Component({
    selector: 'pn-accordion',
    templateUrl: './accordion.html',
    standalone: true,
    imports: [ImportsModule]
})
export class AccordionComponent {}
