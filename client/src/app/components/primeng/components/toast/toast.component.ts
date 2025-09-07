import { Component } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ConfirmationService, MessageService } from 'primeng/api';

@Component({
    selector: 'pn-toast',
    templateUrl: './toast.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class ToastComponent {
    constructor(private messageService: MessageService, private confirmationService: ConfirmationService) {}
    ngOnInit() {}
    showSuccessToast(message: string, title: string = 'Successful'): void {
        this.messageService.add({
            severity: 'success',
            summary: title,
            detail: message,
            life: 3000
        });
    }
    showInfoToast(message: string, title: string = 'Failed'): void {
        this.messageService.add({
            severity: 'info',
            summary: title,
            detail: message,
            life: 3000
        });
    }
    showErrorToast(message: string, title: string = 'Failed'): void {
        this.messageService.add({
            severity: 'error',
            summary: title,
            detail: message,
            life: 3000
        });
    }

    showConfirmation(message: string, header: string = 'Confirm', cb) {
        this.confirmationService.confirm({
            message: message,
            header: header,
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                cb();
            }
        });
    }
}
