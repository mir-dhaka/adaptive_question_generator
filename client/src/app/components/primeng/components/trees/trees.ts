import { Component } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { ActivatedRoute, UrlSegment } from '@angular/router';
import { DataService } from '../../../../services/data.service';

@Component({
    selector: 'pn-trees',
    templateUrl: './trees.html',
    standalone: true,
    imports: [ImportsModule]
})
export class TreesComponent {
    urlSegments: string[] = [];
    itemName: string;
    slug: string;
    itemDialog: boolean;
    items: any[] = [];
    item: any;
    submitted: boolean;
    update: boolean;
    ddParentList: any;
    constructor(
        private route: ActivatedRoute,
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }
    ngOnInit() {
        this.route.url.subscribe((urlSegments: UrlSegment[]) => {
            this.urlSegments = urlSegments.map((segment) => segment.path);
            console.log(this.urlSegments);
        });
        if (this.urlSegments.length > 0) {
            this.itemName = this.urlSegments[this.urlSegments.length - 1];
        }
        this.resolveSlug();
        if (this.slug.length == 0) {
            setTimeout(() => {
                this.messageService.add({
                    severity: 'error',
                    summary: 'Unknown Operation',
                    detail: `${this.itemName} is not valid entity`,
                    life: 3000
                });
            }, 1000);
        } else {
            setTimeout(() => {
                this.loadItems(true);
            }, 300);
        }
    }
    toTitle(inputString: string): string {
        if (!inputString) return inputString;

        // Split the string by dashes and capitalize each word
        let words = inputString.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase());

        // Join the words with spaces
        return words.join(' ');
    }
    resolveSlug() {
        switch (this.itemName.toLowerCase()) {
            case 'trees':
                this.slug = 'trees';
                break;
            default:
                this.slug = '';
        }
    }

    getPlantationDDItems() {
        this.service.getAll("plantations", (res) => {
            if (res.success == true) {
                this.ddParentList = res.data.filter((x) => (x.status != -1));
            } else {
                this.ddParentList = [];
            }
        });
    }
    loadItems(showToast: boolean = false) {
        this.service.getAll(this.slug, (res) => {
            if (res.success == true) {
                this.items = res.data.filter((x) => x.status != -1).map(item => {
                    item.lastHarvestedAt = this.formatDate(item.lastHarvestedAt);
                    item.nextHarvestingAt = this.formatDate(item.nextHarvestingAt);
                    return item;
                });
                if (showToast) {
                    this.showSuccessToast(`${this.itemName} loaded successfully`);
                }
            } else {
                this.items = [];
                this.showErrorToast(`Failed to load ${this.itemName}`, 'Load Data');
            }
        })
    }
    formatDate(dateString: string): string {
        const date = new Date(dateString);
        return `${date.toLocaleDateString()}`;
    }
    saveItem() {
        this.submitted = true;
        if (!this.item.description) this.item.description = ""
        this.item.plantation = null
        if (this.update) {
            this.service.update(this.slug, this.item, (res) => {
                if (res.success == true) {
                    this.showSuccessToast(`${this.itemName} updated`);
                    this.loadItems();
                    this.hideDialog();
                } else {
                    this.showErrorToast(`Failed to update ${this.itemName}`, `Update`);
                }
            });
        } else {
            this.service.create(this.slug, this.item, (res) => {
                if (res.success == true) {
                    this.showSuccessToast(`${this.itemName} inserted`);
                    this.loadItems();
                    this.hideDialog();
                } else {
                    this.showErrorToast(`Failed to insert ${this.itemName}`, `Insert`);
                }
            });
        }
    }

    deleteSelectedItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    deleteItem(item: any) {
        this.confirmationService.confirm({
            message: 'Are you sure you want to delete ' + item.name + '?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.submitted = true;
                this.service.delete(this.slug, item.id, (res) => {
                    if (res.success == true) {
                        this.showSuccessToast(`${this.itemName} Deleted`, 'Delete');
                        this.loadItems();
                    } else {
                        this.showErrorToast(`Failed to delete ${this.itemName}`, 'Delete');
                    }
                });
            }
        });
    }

    importItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    exportItems() {
        this.showInfoToast(`Feature is not implemented yet.`);
    }

    openNew() {
        this.item = {};
        this.update = false;
        this.submitted = false;
        this.itemDialog = true;
        this.getPlantationDDItems()
    }
    editItem(item: any) {
        this.update = true;
        this.item = { ...item };
        this.itemDialog = true;
        console.log(this.item)
        this.getPlantationDDItems()
    }
    hideDialog() {
        this.itemDialog = false;
        this.submitted = false;
    }
    showSuccessToast(message: string, title: string = 'Success'): void {
        this.messageService.add({
            severity: 'success',
            summary: title,
            detail: message,
            life: 3000
        });
    }
    showInfoToast(message: string, title: string = 'Info'): void {
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
}
