import { Component } from '@angular/core';
import { ImportsModule } from '../../../../components/primeng/imports';
import { ConfirmationService, MessageService } from 'primeng/api';
import { DataService } from '../../../../services/data.service';

@Component({
    selector: 'pn-newexam',
    templateUrl: './newexam.component.html',
    standalone: true,
    imports: [ImportsModule]
})
export class NewExamComponent {
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
    examInfoResolved: boolean = false;

    exam_info: string = "";
    exam_action_text: string = "";
    selectedExam: any;
    examDialog: boolean = false;

    currentQuestion: any;
    selectedAnswer: any;

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
    showExamInfo(event: any) {
        this.service.getAll('exams', (res) => {
            this.selectedProfileObj = this.profileList.find(p => p.user_id == this.selectedProfile);
            if (res.success == true) {
                if (res.data.length == 0) {
                    this.selectedExam = null;
                } else {
                    const convertedDataList = this.convertExamData(res.data);
                    this.selectedExam = convertedDataList
                        .find(d => d.student_id == this.selectedProfileObj.profile_id &&
                            d.exam_info.finished == false &&
                            d.exam_info.dag_id == this.selectedProfileObj.dag_id
                        );
                }
                if (this.selectedExam) {
                    this.exam_info = "Resume previous Exam";
                    this.exam_action_text = "Resume";
                } else {
                    this.exam_info = "New Exam on: " + this.selectedProfileObj.dag_title;
                    this.exam_action_text = "Start";
                }
                this.examInfoResolved = true;
            } else {
                this.profileList = [];
            }
        });
    }
    convertExamData(data: any[]): { id: any, student_id: any, exam_info: any }[] {
        return data.map(d => {
            let decodedInfo: any = null;
            decodedInfo = JSON.parse(atob(d.exam_info));
            return {
                id: d.id,
                student_id: d.student_id,
                exam_info: decodedInfo
            };
        });
    }
    startExam() {
        if (!this.selectedExam) {
            const examInfo = { finished: false, dag_id: this.selectedProfileObj.dag_id };
            const newExam = {
                student_id: this.selectedProfileObj.profile_id,
                exam_info: btoa(JSON.stringify(examInfo))
            };
            this.service.upsert("exams", newExam, (res) => {
                this.selectedExam = res.data;

                this.setNextQuestion();
                this.examDialog = true;
            });
        } else {
            this.setNextQuestion();
            this.examDialog = true;
        }

    }
    submitAnswer() {
        if (this.selectedAnswer) {
            const answer = {
                kc_id: this.currentQuestion.kc_id,
                exam_id: this.selectedExam.id,
                question_id: this.currentQuestion.id,
                option_id: this.selectedAnswer.id,
                is_correct: this.selectedAnswer.order==this.currentQuestion.correct_option
            }; 
            this.service.process('save-exam-details', answer, (res) => { 
                if (res.body.success == true) {
                    this.showInfoToast(`Answer recorded successfully`, `Save`);
                    this.setNextQuestion();
                } else {
                    this.showErrorToast(`Failed to save answer`, `Save`);
                }
            });
        } else {
            this.showInfoToast("Please select an option first.", "Submit");
        }
    }
    setNextQuestion() {
        const payload = {
            user_id: this.selectedProfileObj.user_id,
            dag_id: this.selectedProfileObj.dag_id,
            exam_id:this.selectedExam?.id
        };

        this.service.process('get-next-question', payload, (res) => {
            if (res.body.success == true) {
                this.currentQuestion = res.body.data;
            } else {
                this.currentQuestion = this.get_dummy_question();
            }
            this.selectedAnswer = null;
        });
    }

    get_dummy_question() {
        return {
            title: "Failed to get questions!",
            options: []
        };
    }

    finishExam() {
        this.confirmationService.confirm({
            message: 'Are you sure you want to finish the exam?',
            header: 'Confirm',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
                this.service.process("finish-exam", { id: this.selectedExam.id }, (res) => {
                    if (res.body.success == true) {
                        this.showSuccessToast(`Exam finished successfully.`);
                        this.examDialog = false;
                    } else {
                        this.showErrorToast(`Failed to finish exam`, `Finish`);
                    }
                });

            }
        });
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
