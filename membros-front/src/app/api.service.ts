import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  /*
  Aqui é onde de fato, a api do rest é invocada, para acessar os dados do projeto django.
  Aqui é chamado os métodos de obter todos os membros, obter um membro, e salvar novo membro.
  */
  baseUrl = 'http://localhost:8000/';
  // api token do rest framework:
  token = 'Token c82d3a152727b058a9c793d1cfae0895ab5ade20';
  httpHeaders = new HttpHeaders().set('Content-Type', 'application/json').set('Authorization', this.token);

  constructor(private http: HttpClient) { }

  getAllMembers() : Observable<any> {
    return this.http.get(this.baseUrl + 'members/', 
    {headers: this.httpHeaders});
  };

  getMember(id) : Observable<any> {
    return this.http.get(this.baseUrl + 'members/' + id + '/',
    {headers: this.httpHeaders});
  };

  saveNewMember(member) : Observable<any> {
    return this.http.post(this.baseUrl + 'members/', member,
    {headers: this.httpHeaders});
  };

  getAllEvents() : Observable<any> {
    return this.http.get(this.baseUrl + 'events/', 
    {headers: this.httpHeaders});
  };

  getEvent(id) : Observable<any> {
    return this.http.get(this.baseUrl + 'events/' + id + '/',
    {headers: this.httpHeaders});
  };

  // metodos para Event:
  saveNewEvent(member) : Observable<any> {
    return this.http.post(this.baseUrl + 'events/', member,
    {headers: this.httpHeaders});
  };

}

