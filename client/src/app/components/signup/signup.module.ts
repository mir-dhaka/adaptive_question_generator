import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { TranslateModule } from '@ngx-translate/core';

import { SignupRoutingModule } from './signup-routing.module';
import { SignupComponent } from './signup.component';
import { FormModule } from '../layout/form/form.module';
import { ToastComponent } from '../primeng/components/toast/toast.component';

@NgModule({
    imports: [CommonModule, FormsModule, TranslateModule, SignupRoutingModule, ToastComponent],
    declarations: [SignupComponent]
})
export class SignupModule {}
