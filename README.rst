.. raw:: html
   
   <h1 align="center">Automatic Detection of Usability Smells Through the Analysis of Interaction Logs</h1>
   <p align="center"><strong>Bachelor's Degree in “Computer Science and Digital Communication”</strong></>
   <p align="center">
     <a href="https://doi.org/10.1007/978-3-030-85613-7_19">
       <img src="https://shields.io/badge/DOI-10.1007/978--3--030--85613--7__19-lightgrey?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA+9pVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ1dWlkOjVEMjA4OTI0OTNCRkRCMTE5MTRBODU5MEQzMTUwOEM4IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjRGNUMwNzEzQ0M0OTExRTI4OUFBQTI3QkYxMDJGREUyIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjRGNUMwNzEyQ0M0OTExRTI4OUFBQTI3QkYxMDJGREUyIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCBDUzUgTWFjaW50b3NoIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MDc4MDExNzQwNzIwNjgxMTg4QzY4NDUwNDRBQjhGRDgiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6Rjc3RjExNzQwNzIwNjgxMTg4QzZEMjNGNjVBREJBMTciLz4gPGRjOnRpdGxlPiA8cmRmOkFsdD4gPHJkZjpsaSB4bWw6bGFuZz0ieC1kZWZhdWx0Ij5ET0lfZGlzY19sb2dvPC9yZGY6bGk+IDwvcmRmOkFsdD4gPC9kYzp0aXRsZT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6y4GEAAAAEKklEQVR42qyWbWgcVRSG33tnd7Mxie12E+1m0yRqYjClfiCC+EOpWtJi/KxSMbVIRSzYYlUUBYttoWBBf1SkaEFBqvjDij+aVpIWipEK0qa2DfiFmNbYrGlqzCbppsnO3Ot7ZiYxiZtGJANPZjN39r3nvOfcezfitl6Py1y15BGygtSTRPh8gPxE2skXpGfmF50rgF37PEQuI/wGeZgsKDC+iNSR+8hWso9sI+dmvqgLfHkNOUqemkV85iVZPUO+IQ9NHVAFJniOfEoqNUec4gCt55qDUtathjvyGczY+kAa8CymWbSavCNvKwoODANtHZ4/0HSLg0QZNcws+jYPxBdDXX13xA6efg+DXRmY6Jd9WTs5QRV5fyIj7dDMAYsXPwwmaN+mkVyo4BWcgGF649CNr0FVNgO5nqjpWPWBGR+76dcM+ieSlwIlpxWHWZbEA7Sawx7fj0vhfRTK2pSx2BKPBRalyWMiomLSX/CfRp0CWmacjIUvMR3FuxP3MV1boXpbYYd+9CdzopGWHS1qu0yw2nFQlqcbh781OHXGIl3OKicUHOY3aQsjQ2kddPpBpnUtkM/C/nEItv+rII/SBkZ1JVRZPezYBRgXi5ZUqPsj9LvpIoPasNtF+0mD4VHrJ11VrsTdoIO8HJBaCWfp2xT5p3NV7VrYM3thTmyGSjVB1W+CHTgOe74DEp3nqZVaRdGwp83DgeMG4tkLDzjYvTGKmgqF3Lg44ULFU8CyNwPx4Z9hTr8Oe25/OMmTUOlmNlJ2ei2C67oIbU0c6TKM1uKeGx3sWE/XaOvSSoVHd+Zh2CFY0MiIyv1MvM6NwJ/HYLs/go5XQCVvh7pqOWzu90IdUKqNB5V3GSj9WEJbIIWmZYkS1lpqaTngFIXRcWA0wwEOeheBS+eD5/K/KtxqOlKEbDqpEGEbHew0OHrM4Lc+i3cPepDaaCcKjJwN+j2WgL7hZRa5Gqr6CUZ+V7AS/vqOf7xC+jnpol+evtepPXTKoJvCj7/l+t0z5gb9n3Nj8LI/AL172Vrr6Pk6ODVrGXG4hFgT2/M5C7whDLlo6gRnnS1rkqnqSrWiMa1wYciy0ArLajQ2NztwuZlUMbtVt0awMMd2dFmPogq/y6QV0dcOc/IV2tbLNq3zM7TZLqD/62CNQO1SPA+u4afvaXMc3FJGqVEcDzeNcA2wTtyHTLAW2Ov+4jJ5fy1A0QQdk80utEmL8X5upEFkuskBqZ8UujgWCErzyN0XlwUhlkgxfeGhYDJ/q40G9ZGI5bOe3ALkIMqo8ETjMkQnKcH8XIPkZqnBxGYnx99LmL9rk4jPPNFku94+D+Kvko9nOzLlHH6ejPwPYdkrniU75zqT5VRbTtpk7f4HYbYPWsmdZM+/Tos5frbcRlrIHWTxlCaQDDPhj4NPyInZBP4WYADz7myBmAF10gAAAABJRU5ErkJggg==" alt="DOI: 10.1007/978-3-030-85613-7_19" />
     </a>
   </p>

   <p align="center">
      Andrea Esposito (677021)<br>
      <small>Author</small><br>
      <a href="mailto:a.esposito39@studenti.uniba.it">a.esposito39@studenti.uniba.it</a>
   </p>
   <p align="center">
      Prof. Giuseppe Desolda<br>
      Supervisor<br>
      <a href="mailto:giuseppe.desolda@uniba.it">giuseppe.desolda@uniba.it</a>
   </p>

********

The project tracked in this repository has been expanded, and it is now tracked
in multiple repository in the organization account
`SERENE <https://github.com/uxsad>`_.
Note that the frontend was not available in the original version, and a
reference to it has been added only to help people find the relevant
information in the organization account.
        
The Structure of the Repository
===============================

``emotions/``
   This folder contains the Emotion Analysis Tool (written in C++).

``extension/``
   This folder contains the source code of the browser extension (written in
   TypeScript).

``icon/``
   This folder contains the logo and the icons of the project.

``server/``
   This folder contains the server's source code (written in JavaScript).

Code Documentation
==================

The code documentation has been moved and is now available in the various
subdirectories and/or submodules' repositories. Please, refer to the specific
commit of the submodule to get the documentation of the original work or refer
to the newest commit to get the latest documentation.
