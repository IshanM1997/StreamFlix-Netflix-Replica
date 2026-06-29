import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { guestGuard } from './core/guards/guest.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/browse', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent),
    canActivate: [guestGuard],
  },
  {
    path: 'signup',
    loadComponent: () => import('./features/auth/signup/signup.component').then(m => m.SignupComponent),
    canActivate: [guestGuard],
  },
  {
    path: 'browse',
    loadComponent: () => import('./features/browse/browse.component').then(m => m.BrowseComponent),
    canActivate: [authGuard],
  },
  {
    path: 'search',
    loadComponent: () => import('./features/search/search.component').then(m => m.SearchComponent),
    canActivate: [authGuard],
  },
  {
    path: 'my-list',
    loadComponent: () => import('./features/my-list/my-list.component').then(m => m.MyListComponent),
    canActivate: [authGuard],
  },
  {
    path: 'watch/:id',
    loadComponent: () => import('./features/player/player.component').then(m => m.PlayerComponent),
    canActivate: [authGuard],
  },
  { path: '**', redirectTo: '/browse' },
];
