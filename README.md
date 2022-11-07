## dolist.sh
dolist is a web app that finds and reports the TODO comments in the repositories. It's currently under construction. 

 **check the app in action**: <a href="http://15.188.137.121" target="_blank">dev env</a>

---

### What is currently possible
- Users can select their GitHub repostiories to start monitoring TODOs
- The app will check the TODOs from the codebase at each push to the main branch of the repo
- Users can see the TODO comments report, TODOs are grouped by status - NEW, OLD, RESOLVED

### Ideas on roadmap
- Support more languages than only JS/TS and Python
- Email notification for a new report
- Create/link issues in the 3rd party ticketing system
- Add a note to the TODO

### Design, Architecture, Data Model
- [Design Library](https://www.figma.com/file/lSDHziGxwbopLfoL8p43Cb/Design-System?node-id=0%3A1)
- [System Architecture](https://drive.google.com/file/d/1QEfP89Zb5kh3Bgez4r786wvwnbHva9Z7/view?usp=sharing)
- [Data Model Diagram](https://drive.google.com/file/d/1MlEYuoKS7iMn3ZGHOVMeb6cs8FxjBBII/view)
