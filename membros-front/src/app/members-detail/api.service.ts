import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  baseUrl = 'http://localhost:8000/';
  // api token do rest framework:
  token = 'Token c82d3a152727b058a9c793d1cfae0895ab5ade20';
  httpHeaders = new HttpHeaders().set('Content-Type', 'application/json').set('Authorization', this.token);


  constructor(private http: HttpClient) { }

  getMember(id) : Observable<any> {
    return this.http.get(this.baseUrl + 'members/' + id + '/',
    {headers: this.httpHeaders});
  };

  updateMember(member) : Observable<any> {
    let body = { name: member.name, surname: member.surname, phone: member.phone};
    return this.http.put(this.baseUrl + 'members/' + member.id + '/', body,
    {headers: this.httpHeaders});
  };


  deleteMember(id) : Observable<any> {
    return this.http.delete(this.baseUrl + 'members/' + id + '/',
    {headers: this.httpHeaders});
  };


}
