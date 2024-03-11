#final


anode = ["A",4,"-o","o","h1+w1+2*w2+4*w3+3*h2+w4","2*h1+w1+2*w2+4*w3+3*h2+w4"]
cathode = ["K",5,"-o","o","0","h1"]
ringDl = ["DL",6,"-o","-r","h1+w1+w2+4*w3+3*h2","h1+w1+2*w2+4*w3+3*h2"]
ringDr = ["DR",7,"r","o","h1+w1+w2+4*w3+3*h2","h1+w1+2*w2+4*w3+3*h2"]
ringEl = ["EL",8,"-o","-r","h1+w1+w2+3*w3+3*h2","h1+w1+w2+3*w3+2*h2"]
ringEr = ["ER",9,"r","o","h1+w1+w2+3*w3+3*h2","h1+w1+w2+3*w3+2*h2"]


stacks = [anode, cathode, ringDl, ringDr, ringEl, ringEr]

def generate_header():
  script = f"""
int CB=3;
real w1 = 1.623, h1 = 0.26, w2 = 0.494, w3 = 1.09, h2 = 0.2, w4 = 0.983, o=4, r=2;

"""
  return(script)

print(generate_header())

def generate_rect(input):
  label,num,x1,x2,y1,y2 = input
  script = f"""
int C{label}={num};
  
border bottom{label}(t={x1},{x2}){{ x=t; y={y1}; label=C{label};}};
border right{label}(t={y1},{y2}){{ x={x2}; y=t; label=C{label};}};
border top{label}(t={x2},{x1}){{ x=t; y={y2}; label=C{label};}};
border left{label}(t={y2},{y1}){{ x={x1}; y=t; label=C{label};}};

  """
  return(script)


for item in stacks:
  print(generate_rect(item))

def get_mesh(input):
  label, num, x1, x2, y1, y2 = input
  script = f"""bottom{label}({x1}*n)+top{label}({x1}*n)+right{label}(-({y2})*n)+left{label}(-({y2})*n)"""
  return script

meshlist = []
for item in stacks:
  meshlist.append(get_mesh(item))

def all_mesh(meshlist):
    line = f"""
border enclosure(t=0,2*pi){{x=10*cos(t); y=10*sin(t); label=CB;}}
int n=15;
mesh Th = buildmesh(enclosure(3*n)"""
    for mesh in meshlist:
      line += "+" + mesh
    line += ")"
    return line

print(all_mesh(meshlist))



label_list = []
for item in stacks:
  label_list.append("C"+item[0])
print(label_list)

def solve_field(label_list):
    script = f"""
fespace Vh(Th,P1);
Vh u,v;
real u0=1000;
problem Electro(u,v) = int2d(Th)(dx(u)*dx(v) + dy(u)*dy(v))"""
    for label in label_list:
      script+="+on("+label+", u=0)"
    script+=";"
    script+= """real error=0.01;
for (int i=0;i<1;i++){
   Electro;
   Th=adaptmesh(Th,u,err=error);
   error=error/2.0;
}
Electro;

Vh Ex, Ey;
Ex = -dx(u);
Ey = -dy(u);

plot(u,value=true);"""
    return script

print(solve_field(label_list))



