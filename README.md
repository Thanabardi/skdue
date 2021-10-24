# skdue
[![Build Status](https://app.travis-ci.com/patkamon/skdue.svg?branch=apply-ci)](https://app.travis-ci.com/patkamon/skdue) [![codecov](https://codecov.io/gh/patkamon/skdue/branch/apply-ci/graph/badge.svg?token=5EZP9GP4CX)](https://codecov.io/gh/patkamon/skdue)


## Description

**Skdue** is a web application that makes your life easier by helping you manage your schedule. With the ability which allows you to create and manage your activities and events, you will never miss any of them. What makes Skdue stand out from the other calendar applications is the feature that lets you follow your favorite people, companies, or celebrities and add their events to your schedule.

## Team Members

| Name    | GitHub                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------- |
| Ditthapong         | [HuskyIsHere](https://github.com/HuskyIsHere)  |
| Kittison  | [touchtool](https://github.com/touchtool)                                           |
| Natchanon | [natchanon-space](https://github.com/natchanon-space)                                                    |
| Patkamon | [patkamon](https://github.com/patkamon)                                                    |
| Thanabardi | [Thanabardi](https://github.com/Thanabardi)                                                     |

## Setup
<details>
  <summary> Django Setup </summary>
  <p>

  ```
  # activate virtual environment
  source venv/bin/activate
  ```
  ```
  # install dependencies
  pip install -r requirements.txt
  ```
  ```
  # setup database
  python manage.py migrate
  python manage.py loaddata calendar_data
  ```
  ```
  # run server and explorer api
  python manage.py runserver
  ```
  </p>
    </details>

<details>
  <summary> Vue Setup </summary>
  <p>  

  ```
  # install vue
  npm install -g @vue/cli
  ```
  ```
  # install dependencies
  cd calendar_vue
  npm install
  ```
  ```
  # run frontend sever
  npm run serve
  ```
  </p>
    </details>


## Iteration Plan

- [Iteration 1](/../../wiki/Iteration-Plan-1)
- [Iteration 2](/../../wiki/Iteration-Plan-2)
- [Iteration 3](/../../wiki/Iteration-Plan-3)
- [Iteration 4](/../../wiki/Iteration-Plan-4)
- [Iteration 5](/../../wiki/Iteration-Plan-5)

## Project Documents

* [Project Proposal](https://docs.google.com/document/d/1ZdIS9-_TD_CAAROzRfGB1QxAL8mmSFebVxw4AjWr2yQ/edit#heading=h.pe6wpztc0dwa)
* [Project Jamboard](https://jamboard.google.com/d/1iB_wpYj0qTMekB9jfVZLBmZ4JiU3f6bvgBLjktGU23o/edit?usp=sharing)
* [Django Rest Model](https://drive.google.com/file/d/1Xu2_mMAfK72p_U584PJ2d0ifFIC8Fjo2/view?usp=sharing)
* [Vision Statement](./Vision-Statement)

  [readmore](/../../wiki#project-documents)
