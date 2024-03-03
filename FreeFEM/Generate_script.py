def generate_rect(label,num,x1,x2,y1,y2):
    script = f"""
int C{label}={num}

border bottom{label}(t={x1},{x2}){{ x=t; y={y1}; label=C{label};}};
border right{label}(t={y1},{y2}){{ x={x2}; y=t; label=C{label};}};
border top{label}(t={x1},{x2}){{ x=t; y={y2}; label=C{label};}};
border left{label}(t={y2},{y1}){{ x={x1}; y=t; label=C{label};}};


//add to mesh
bottom{label}(-({x1})*n)+top{label}(-({x1})*n)+right{label}(-({y2})*n)+left{label}(-({y2})*n))

"""
    return(script)
