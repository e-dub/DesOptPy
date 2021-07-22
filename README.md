# DesOptPy2

## Checklist

### General
- [x] Ask Veit and Johannes for what he would like as user
- [x] new github repository
- [ ] Update logo
- [ ] Release
- [ ] Publish on Open Source Software?

### Examples
- [ ] set up example with SiMuLi
- [ ] set up example with EasyBeam
- [ ] set up example with Kratos
- [ ] set up example with Ansys (pyAnsys)

### Code general
- [x] variable function for primal and sens
- [x] different way to define design variables with x vector
- [x] add initial step to calc nx, ng and source of algorithm!
- [ ] make all values numpy arrays
- [ ] return arrays!!! not lists, for gradients important!
- [ ] remove parameter pyOptAlg = True
- [ ] add option, fType min max
- [ ] normalize and denormalize as vector operations? not index assignment?`
- [ ] test gradients that they work well!!!
- [ ] nit for nongrad alg
- [ ]  ResultReport
- [ ] sensitivity analysis
- [ ]  Postprocessing for shadow prices
- [ ] echo or debug level? what is standard?
- [ ]  Variable linking?

### File handling
- [x]  File handling save all evaluation data
- [x]  File handling and run results folder (no run only modelname with time stamp)
- [ ]  filehandling for saving all evaluation to find if it is a new iteration or a finite differencing iteration (or also step length)

### History etc
- [x] read in history at end
- [ ]  renorm etc with history!!! Iteration values, Optimal values

### Algorithms
- [ ] add pygmo
- [ ] add deap
https://deap.readthedocs.io/en/master/tutorials/advanced/constraints.html
- [ ] add cvxopt
http://cvxopt.org/userguide/index.html
- [ ] add nlopt
https://nlopt.readthedocs.io/en/latest/
- [x]  add scipy optimization
- [ ]  add or-tools?
- [ ]  add Hybrid Cellular Automata
https://developers.google.com/optimization/introduction/pythonself.xL
- [x] add algorithm list?
- [ ]  Algorithm options
- [x] add avail optimization algorithms, updated by setup? possible?
- [ ] scipy also without gradients
- [ ] pyopt interface different file

### Surrogating
- [ ]  surrogating?
- [ ]  sampling and ploting of design space

### Monitoring
- [ ]  Optimization live monitoring!
- [ ] bokeh stream
https://www.youtube.com/watch?v=WgyTSsVtc7o





