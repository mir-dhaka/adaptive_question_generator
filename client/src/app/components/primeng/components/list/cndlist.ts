import { Component } from '@angular/core';
import { ImportsModule } from '../../imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { ActivatedRoute, UrlSegment } from '@angular/router';
import { DataService } from '../../../../services/data.service';

@Component({
    selector: 'pn-cndlist',
    templateUrl: './cndlist.html',
    standalone: true,
    imports: [ImportsModule]
})
export class CNDListComponent {
    urlSegments: string[] = [];
    itemName: string;
    slug: string;
    itemDialog: boolean;
    isHeirchyData: boolean;
    heirchyParentList: any[] = [];
    hLevel: any;
    items: any[] = [];
    item: any;
    selectedParent: any;
    selectedItems: any[] = [];
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
        this.isHeirchyData = false
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
    resolveSlug() {
        switch (this.itemName.toLowerCase()) {
            case 'roles':
                this.slug = 'roles';
                break;
            case 'permissions':
                this.slug = 'permissions';
                break;
            case 'users':
                this.slug = 'users';
                break;
            case 'divisions':
                this.slug = 'areas';
                this.isHeirchyData = true;
                this.hLevel = { level: 0 };
                break;
            case 'zones':
                this.slug = 'areas';
                this.isHeirchyData = true;
                this.hLevel = { parentHeader: 'Division', level: 1 };
                break;
            case 'areas':
                this.slug = 'areas';
                this.isHeirchyData = true;
                this.hLevel = { parentHeader: 'Zone', level: 2 };
                break;
            case 'blocks':
                this.slug = 'areas';
                this.isHeirchyData = true;
                this.hLevel = { parentHeader: 'Area', level: 3 };
                break;
            case 'sub-blocks':
                this.slug = 'areas';
                this.isHeirchyData = true;
                this.hLevel = { parentHeader: 'Block', level: 4 };
                break;
            case 'grades':
                this.slug = 'grades';
                break;
            case 'qualities':
                this.slug = 'qualitys';
                break;
            case 'basicdatatypes':
                this.slug = 'basicdatatypes';
                break;
            case 'basicdatas':
                this.slug = 'basicdatas';
                break;
            case 'fruits-collection-points':
                this.slug = 'FCPs';
                break;
            default:
                this.slug = '';
        }
    }
    getParentDDItems() {
        this.service.getMany(this.slug, {
            "Level": {
                "operator": "eq",
                dataType: "System.Int32",
                value: (this.hLevel.level - 1)
            }
        }, (res) => {
            if (res.success == true) {
                this.heirchyParentList = res.data.filter((x) => (x.status != -1));
            } else {
                this.heirchyParentList = [];
            }
        });
    }
    getSubBlockDDItems() {
        this.service.getMany("areas", {
            "Level": {
                "operator": "eq",
                dataType: "System.Int32",
                value: 4
            }
        }, (res) => {
            if (res.success == true) {
                this.ddParentList = res.data.filter((x) => (x.status != -1));
            } else {
                this.ddParentList = [];
            }
        });
    }
    loadItems(showToast: boolean = false) {
        if (this.isHeirchyData) {
            this.service.getMany(this.slug, {
                "Level": {
                    "operator": "eq",
                    dataType: "System.Int32",
                    value: this.hLevel.level
                }
            }, (res) => {
                if (res.success == true) {
                    this.items = res.data.filter((x) => (x.level == (this.hLevel.level) && x.status != -1));
                    if (showToast) {
                        this.showSuccessToast(`${this.itemName} loaded successfully`);
                    }
                } else {
                    this.items = [];
                    this.showErrorToast(`Failed to load ${this.itemName}`, 'Load Data');
                }
            });
        }
        else {
            this.service.getAll(this.slug, (res) => {
                if (res.success == true) {
                    this.items = res.data.filter((x) => x.status != -1);
                    if (showToast) {
                        this.showSuccessToast(`${this.itemName} loaded successfully`);
                    }
                } else {
                    this.items = [];
                    this.showErrorToast(`Failed to load ${this.itemName}`, 'Load Data');
                }
            });
        }
    }
    saveItem() {
        this.submitted = true;
        if (this.isHeirchyData) {
            this.item.level = this.hLevel.level
            this.item.parent = null;
            this.item.parentId = this.selectedParent ? this.selectedParent : null
        }
        if (!this.item.description) this.item.description = ""
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
        this.selectedParent = ''
        if (this.hLevel.level !== 0) {
            this.getParentDDItems()
        }
        if (this.slug == "FCPs") {
            this.getSubBlockDDItems()
        }
    }
    editItem(item: any) {
        this.update = true;
        this.item = { ...item };
        this.itemDialog = true;
        this.selectedParent = this.item.parentId
        if (this.hLevel.level !== 0) {
            this.getParentDDItems()
        }
        if (this.slug == "FCPs") {
            this.getSubBlockDDItems()
        }
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
