import { Component } from '@angular/core';
import { ImportsModule } from '../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../services/data.service';
import { NgChartsModule } from 'ng2-charts';

@Component({
    selector: 'pn-examdetails',
    templateUrl: './examdetails.component.html',
    standalone: true,
    imports: [ImportsModule, NgChartsModule]
})
export class ExamDetailsComponent {
    private _slug: string;
    public get slug(): string {
        return this._slug;
    }
    public set slug(value: string) {
        this._slug = value;
    }

    profileList: any[] = [];
    selectedProfile: any;
    selectedProfileObj: any;

    examList: any[] = [];
    selectedExam: any;
    selectedExamObj: any;

    examDetails: any;

    constructor(
        private messageService: MessageService,
        private confirmationService: ConfirmationService,
        private service: DataService
    ) { }

    ngOnInit() {
        this.service.process('get-student-dag-info', {}, (res) => {
            if (res.body.success == true) {
                this.profileList = res.body.data;
            } else {
                this.profileList = [];
            }
        });
    }

    getExamInfo(event: any) {
        this.service.process('get-exam-info', { student_id: event.value }, (res) => {
            if (res.body.success == true) {
                this.examDetails = null;
                this.examList = res.body.data;
                if (this.examList.length > 0) {
                   // this.showSuccessToast("Exam information loaded", "Info");
                } else {
                    this.showErrorToast("No Exams found for this profile", "Info");
                }
            } else {
                this.examList = [];
                this.showErrorToast("Failed to load exam information", "Info");
            }
        });
    }

    showExamDetailInfo(event: any) {
        this.service.process('get-exam-detail-info', { id: event.value }, (res) => {
            if (res.body.success == true) {
                this.examDetails = res.body.data;
                if (this.examDetails) { 
                    this.showSuccessToast("Exam detail information loaded", "Info");
                    this.setMasteryChartData(this.examDetails.mastery);

                } else {
                    this.showErrorToast("No Exam details found", "Info");
                }
            } else {
                this.examDetails = null;
                this.showErrorToast("Failed to load exam detail information", "Info");
            }
        });
    }

    groupByQuestions(info: any[]): { question_number: number, kc: string, question: string, answers: any[] }[] {
        const grouped: { question_number: number, kc: string, question: string, answers: any[] }[] = [];

        info.forEach((item, index) => {
            grouped.push({
                question_number: index + 1,  // sequential numbering
                kc: item.kc,
                question: item.question,
                answers: [
                    {
                        answer: item.answer,
                        correct_answer: item.correct_answer,
                        is_correct: item.is_correct
                    }
                ]
            });
        });

        return grouped;
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
