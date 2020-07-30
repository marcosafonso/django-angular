import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
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

  
  getEvent(id) : Observable<any> {
    return this.http.get(this.baseUrl + 'events/' + id + '/',
    {headers: this.httpHeaders});
  };

  updateEvent(event) : Observable<any> {
    let body = { name: event.name, describe: event.describe};
    return this.http.put(this.baseUrl + 'events/' + event.id + '/', body,
    {headers: this.httpHeaders});
  };

  deleteEvent(id) : Observable<any> {
    return this.http.delete(this.baseUrl + 'events/' + id + '/',
    {headers: this.httpHeaders});
  };

}
