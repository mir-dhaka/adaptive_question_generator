import { Component, OnInit, ViewChild } from '@angular/core';
import { routerTransition } from '../router.animations';
import { AuthService } from '../../services/auth.service';
import { RegistrationModel } from '../../models/auth.models';
import { ToastComponent } from '../primeng/components/toast/toast.component';

@Component({
    selector: 'app-signup',
    templateUrl: './signup.component.html',
    styleUrls: ['./signup.component.scss'],
    animations: [routerTransition()]
})
export class SignupComponent implements OnInit {
    @ViewChild(ToastComponent) toast: ToastComponent;
    title: string;
    password2: string;
    model: RegistrationModel = {
        first_name: '',
        last_name: '',
        user_name:'',
        email: '',
        password: '',
        role:''
    };
    constructor(private service: AuthService) {
        this.title = 'Adaptive Learning';
    }

    ngOnInit() {}

    register() {
        if (this.model.password != this.password2) {
            this.toast.showErrorToast('Passwords must match');
            return;
        } 
        this.model.user_name=this.model.email;
        this.model.role='student';

        this.service.register(this.model, (res) => { 
            if (res.success == true) {
                this.toast.showSuccessToast(res.message);
            } else {
                this.toast.showErrorToast(res.message);
            }
        });
    }
}
