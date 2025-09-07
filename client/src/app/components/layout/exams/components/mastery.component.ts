import { Component } from '@angular/core';
import { ImportsModule } from '../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../services/data.service';
import { NgChartsModule } from 'ng2-charts';

@Component({
    selector: 'pn-mastery',
    templateUrl: './mastery.component.html',
    standalone: true,
    imports: [ImportsModule, NgChartsModule]
})
export class MasteryComponent {
    private _slug: string;
    public get slug(): string {
        return this._slug;
    }
    public set slug(value: string) {
        this._slug = value;
    }

    examList: any[] = [];

    examDetails: any;

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }

    ngOnInit() {
        this.service.getAll('exams', (res) => {
            if (res.success == true) {
                this.examList = res.data;
                this.showExamDetailInfo(); 
                setInterval(() => {
                    this.showExamDetailInfo();
                }, 5000);
            } else {
                this.examList = [];
            }
        });
    }
    counter = 0;
    showExamDetailInfo() {
        if (this.examList.length == 0)
            return;
        const examId = this.examList[this.counter].id;
        this.counter += 1;

        if (this.counter == this.examList.length) {
            this.counter = 0;
        }

        this.service.process('get-exam-detail-info', { id: examId }, (res) => {
            if (res.body.success == true) {
                this.examDetails = res.body.data;
                if (this.examDetails) {
                    //this.showSuccessToast("Exam detail information loaded", "Info");
                    this.setMasteryChartData(this.examDetails.mastery);

                } else {
                    //this.showErrorToast("No Exam details found", "Info");
                }
            } else {
                this.examDetails = null;
                //this.showErrorToast("Failed to load exam detail information", "Info");
            }
        });
    }

    // mastery chart
    public masteryChartLabels: string[] = [];
    public masteryChartData: any[] = [];
    public masteryChartOptions: any = {
        responsive: true,
        scales: {
            y: {
                min: 0,
                max: 1
            }
        }
    };
    public masteryChartColors: any[] = [
        {
            borderColor: 'pink',
            backgroundColor: 'rgba(255,192,203,0.2)'
        },
        {
            borderColor: 'blue',
            backgroundColor: 'rgba(0,0,255,0.2)'
        }
    ];

    setMasteryChartData(mastery: any[]) {
        this.masteryChartLabels = mastery.map(m => m.kc);
        this.masteryChartData = [
            {
                data: mastery.map(m => m.previous_mastery),
                label: 'Previous Mastery'
            },
            {
                data: mastery.map(m => m.current_mastery),
                label: 'Current Mastery'
            }
        ];
    }
}
