import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../router.animations';

import { DataService } from '../../../services/data.service';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss'],
    animations: [routerTransition()]
})
export class DashboardComponent implements OnInit {
    public alerts: Array<any> = [];
    public sliders: Array<any> = [];
    public counters: Array<any> = [];
    dashboardCounters: any[] = [];
    examDetails: any;
    exams: any[] = [];
    counter: number = 0;
    dag_url: string = "http://localhost:8000/files/dag_2.png";
    dag_label: string = "Functional Programming";

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

    constructor(private service: DataService) {
        this.sliders.push(
            {
                imagePath: 'assets/images/slider1.jpg',
                label: 'First slide label',
                text: 'Nulla vitae elit libero, a pharetra augue mollis interdum.'
            },
            {
                imagePath: 'assets/images/slider2.jpg',
                label: 'Second slide label',
                text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
            },
            {
                imagePath: 'assets/images/slider3.jpg',
                label: 'Third slide label',
                text: 'Praesent commodo cursus magna, vel scelerisque nisl consectetur.'
            }
        );

        this.alerts.push(
            {
                id: 1,
                type: 'success',
                message: `Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Voluptates est animi quibusdam praesentium quam, et perspiciatis,
                consectetur velit culpa molestias dignissimos
                voluptatum veritatis quod aliquam! Rerum placeat necessitatibus, vitae dolorum`
            },
            {
                id: 2,
                type: 'warning',
                message: `Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Voluptates est animi quibusdam praesentium quam, et perspiciatis,
                consectetur velit culpa molestias dignissimos
                voluptatum veritatis quod aliquam! Rerum placeat necessitatibus, vitae dolorum`
            }
        );

        this.counters.push(
            { type: "profiles", count: 85 },
            { type: "kcs", count: 8 },
            { type: "dags", count: 1 },
            { type: "exams", count: 10 },
        );
    }

    ngOnInit() {
        this.service.process('get-dashboard-counter-info', {}, (res) => {
            if (res.body.success == true) {
                this.dashboardCounters = res.body.data;
            } else {
                this.dashboardCounters = [];
            }
        });
        setInterval(() => {
            this.changeDag();
        }, 7000);
    }
    changeDag() {
        if (this.dag_label.indexOf("Python") < 0) {
            this.dag_url = "http://localhost:8000/files/dag_1.png";
            this.dag_label = "Python Programming";
        } else {
            this.dag_url = "http://localhost:8000/files/dag_2.png";
            this.dag_label = "Functional Programming";
        }
    }

    public closeAlert(alert: any) {
        const index: number = this.alerts.indexOf(alert);
        this.alerts.splice(index, 1);
    }

}
