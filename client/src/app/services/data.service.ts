import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BaseService } from './base.service';
import { Injectable } from '@angular/core';
import { v4 as guid } from 'uuid';
import { of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ObjectUtil } from '../utils/objectUtil';

@Injectable({
    providedIn: 'root'
})
export class DataService extends BaseService {
    constructor(public http: HttpClient) {
        super('/data', http);
    }

    getOne(slug: string, id: guid, cb) {
        this._getOne(slug, id)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred get-one. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    getAll(slug: string, cb) {
        this._getAll(slug)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred get-all. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    getMany(slug: string, filterObj: any, cb) {
        this._getMany(slug, filterObj)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred get-many. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    create(slug: string, data: any, cb) {
        this._create(slug, data)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred on create. slug: ${slug}`, error);
                    return of({ body: this._getErrorResponse() });
                })
            )
            .subscribe((res: any) => {
                cb(res.body);
            });
    }
    upsert(slug:string, data:any,cb){
         if (ObjectUtil.hasProperties(data, ['id'])) {
            this.update(slug,data,cb);
         }else{
            this.create(slug,data,cb);
         }
    }

    update(slug: string, data: any, cb) {
        this._update(slug, data)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred on update. slug: ${slug}`, error);
                    return of({ body: this._getErrorResponse() });
                })
            )
            .subscribe((res: any) => {
                cb(res.body);
            });
    }

    delete(slug: string, id: guid, cb) {
        this._delete(slug, id)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred on delete. slug: ${slug}`, error);
                    return of({ body: this._getErrorResponse() });
                })
            )
            .subscribe((res: any) => {
                cb(res.body);
            });
    }

    process(slug: string, data: any, cb) {
        this._process(slug, data)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred on process. slug: ${slug}`, error);
                    return of({ body: this._getErrorResponse() });
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    ddata(slug: string, filterObj: any, cb) {
        this._getDData(slug, filterObj)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred in get-ddata. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    ddl(slug: string, filterObj: any, cb) {
        this._getDdl(slug, filterObj)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred in get-ddata. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }

    report(slug: string, filterObj: any, cb) {
        this._getReport(slug, filterObj)
            .pipe(
                catchError((error) => {
                    console.error(`Error occurred in get-ddata. slug: ${slug}`, error);
                    return of(this._getErrorResponse());
                })
            )
            .subscribe((res: any) => {
                cb(res);
            });
    }
}
