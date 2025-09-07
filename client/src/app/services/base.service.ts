import { Observable, forkJoin } from 'rxjs';
import { HttpResponse, HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { v4 as guid } from 'uuid';

import { environment as env } from '../../environments/environment';
import { ObjectUtil } from '../utils/objectUtil';
import { EntityStatus } from '../models/core.models';

export abstract class BaseService {
    dumbData: boolean = false;
    constructor(public apiURL: string, public http: HttpClient, dumpData: boolean = false) {
        this.apiURL = env.apiHost + env.apiPrefix + apiURL;
        this.dumbData = dumpData;
    }

    dumpResponseBody(data) {
        if (this.dumbData){
            let info= `url: ${this.apiURL} data: ${JSON.stringify(data)}`;
            console.log(info);
            //alert(info);
        }
          
    }

    get_by_url(url: string) {
        return this.http.get(url);
    }
    post_by_url(url: string, payload: any) { 
        return this.http.post(url, payload, { observe: 'response' });
    }

    _getOne(slug: string, id: guid) {
        return this.http.get(`${this.apiURL}/getone/${slug}/${id}`);
    }
    _getAll(slug: string) {
        return this.http.get(`${this.apiURL}/getall/${slug}`);
    }
    _getMany(slug: string, filterObject: any) {
        const params = this._getHttpParmWithBase64Content(filterObject);
        return this.http.get(`${this.apiURL}/getmany/${slug}`, { params });
    }
    _create(slug: string, data: any): Observable<HttpResponse<Object>> {
        const propertiesToRemove = ['id', 'status', 'createdby', 'createdat', 'editedby', 'editedat'];
        const insertObject = ObjectUtil.removeProperties(data, propertiesToRemove);
        const base64 = btoa(JSON.stringify(insertObject));
        //const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
        return this.http.post(`${this.apiURL}/save/${slug}`, { Data: base64 }, { observe: 'response' });
    }
    _update(slug: string, data: any): Observable<HttpResponse<Object>> {
        if (ObjectUtil.hasProperties(data, ['id'])) {
            const propertiesToRemove = ['createdby', 'createdat', 'editedby', 'editedat'];
            const updateObject = ObjectUtil.removeProperties(data, propertiesToRemove);
            const base64 = btoa(JSON.stringify(updateObject));
            return this.http.post(`${this.apiURL}/save/${slug}`, { Data: base64 }, { observe: 'response' });
        } else {
            console.log(`id is required for update`);
        }
    }
    _delete(slug: string, id: guid): Observable<HttpResponse<Object>> {
        const data = { status: EntityStatus.Deleted };
        const base64 = btoa(JSON.stringify(data));
        return this.http.post(`${this.apiURL}/remove/${slug}/${id}`, { Data: base64 }, { observe: 'response' });
    }
    _process(slug: string, data: any): Observable<HttpResponse<Object>> {
        const base64 = btoa(JSON.stringify(data));
        return this.http.post(`${this.apiURL}/process/${slug}`, { Data: base64 }, { observe: 'response' });
    }
    _getDData(slug: string, filterObject: any) {
        const params = this._getHttpParmWithBase64Content(filterObject);
        return this.http.get(`${this.apiURL}/ddata/${slug}`, { params }); //de-normalized data
    }
    _getDdl(slug: string, filterObject: any) {
        const params = this._getHttpParmWithBase64Content(filterObject);
        return this.http.get(`${this.apiURL}/ddldata/${slug}`, { params }); //de-normalized data
    }
    _getReport(slug: string, filterObject: any) {
        const params = this._getHttpParmWithBase64Content(filterObject);
        return this.http.get(`${this.apiURL}/report/${slug}`, { params });
    }
    _upload(url: string, file: File) {
        // const formData: FormData = new FormData();
        // if (file) {
        //     formData.append('files', file, file.name);
        // }
        // return this.http.post(url, formData);
    }
    _download(url: string, file: File) {
        // const formData: FormData = new FormData();
        // if (file) {
        //     formData.append('files', file, file.name);
        // }
        // return this.http.post(url, formData);
    }
    _method(slug: string, data: any): Observable<HttpResponse<Object>> {
        return this.http.post(this.apiURL + '/method/' + slug, data, { observe: 'response' });
    }

    _gmethod(data: any): Observable<HttpResponse<Object>> {
        return this.http.post(this.apiURL + '/method/GenericMethod', data, { observe: 'response' });
    }
    _fork_gmethod(info: any[]): Observable<any[]> {
        var requests = [];
        for (var k = 0; k < info.length; k++) {
            requests.push(this.http.post(this.apiURL + '/method/GenericMethod', info[k]));
        }
        return forkJoin(requests);
    }

    _cloneObject(obj: any) {
        return JSON.parse(JSON.stringify(obj));
    }

    //error responses
    _getErrorResponse(code: number = 500, message: string = 'An error occured') {
        return { success: false, code: code, message: message };
    }

    //base64
    _getHttpParmWithBase64Content(obj: any, propName: string = 'Data'): HttpParams {
        const base64 = btoa(JSON.stringify(obj));
        const params = new HttpParams().set(propName, base64);
        return params;
    }
}
