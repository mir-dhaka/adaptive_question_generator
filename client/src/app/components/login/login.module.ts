import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
import { FormsModule } from '@angular/forms';
import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { ToastComponent } from '../primeng/components/toast/toast.component';

@NgModule({
    imports: [CommonModule, FormsModule, TranslateModule, LoginRoutingModule, ToastComponent],
    declarations: [LoginComponent]
})
export class LoginModule {}
