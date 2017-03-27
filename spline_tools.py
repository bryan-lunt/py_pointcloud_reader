import scipy as S
import scipy.interpolate as INTERP

def all_spline_stuff(xs,ys,density=2000):
    myspline = INTERP.UnivariateSpline(xs,ys)

    dense_xs = S.linspace(xs[0],xs[-1],density)
    dense_ys = myspline(dense_xs)
    dy_dx = myspline.derivative(1)

    dense_dy_dx_samples = dy_dx(dense_xs)
    dl_dx_samples = S.power(1.0+S.power(dense_dy_dx_samples,2.0),0.5)

    dl_spline = INTERP.UnivariateSpline(dense_xs,dl_dx_samples)

    integrated = list()
    for i in dense_xs:
        integrated.append(dl_spline.integral(0.0,i))
    integrated = S.array(integrated)

    x_to_l = INTERP.UnivariateSpline(dense_xs,integrated)
    l_to_x = INTERP.UnivariateSpline(integrated,dense_xs)
    l_to_y = INTERP.UnivariateSpline(integrated,dense_ys)

    return myspline, {"x_to_l":x_to_l,"l_to_x":l_to_x,"l_to_y":l_to_y}

class ParametricSpline(object):
    def __init__(self,x,y,resample_level=20):
        self.data_x = x
        self.data_y = y

        self.spline_x, self.spline_y = self.update_spline(self.data_x,self.data_y)

    def update_spline(self,x,y,normalize=True,resample_level=1,resample_iterations=1):
        tmp_spline_x = None
        tmp_spline_y = None

        tmp_x = x
        tmp_y = y

        for i in range(resample_iterations):
            dist = S.real( S.sqrt(S.power(tmp_x[:-1] - tmp_x[1:],2.0) + S.power(tmp_y[:-1] - tmp_y[1:],2.0) ))
            dist_along = S.concatenate(([0], dist.cumsum()))
            if normalize:
                dist_along*=S.power(dist_along[-1],-1.0)

            tmp_spline_x = INTERP.UnivariateSpline(dist_along,tmp_x,s=1,k=2)
            tmp_spline_y = INTERP.UnivariateSpline(dist_along,tmp_y,s=1,k=2)

            resample_ts = S.linspace(0.0,dist_along[-1],resample_level*tmp_x.size)

            tmp_x = tmp_spline_x(resample_ts)
            tmp_y = tmp_spline_y(resample_ts)

        return tmp_spline_x, tmp_spline_y

    def __call__(self,t):
        return S.hstack([self.spline_x(t).reshape(-1,1), self.spline_y(t).reshape(-1,1)])

if __name__ == "__main__":
    """test the tools"""

    import pylab

    ap_line = S.array([[-213.1,13.5],
                    [-90.67,5.46],
                    [-52.56,1.54],
                    [-15.34,0.622],
                    [12.9,0.622],
                    [44.75,1.54],
                    [78.38,3.39],
                    [118.3,7.54],
                    [187.8,16.3]])

    x = ap_line[:,0]
    y = ap_line[:,1]

    # x,y coordinates of contour points, not monotonically increasing
    #x = S.array([2.,  1.,  1.,  2.,  2.,  4.,  4.,  3.])
    #y = S.array([1.,  2.,  3.,  4.,  2.,  3.,  2.,  1.])

    # f: X --> Y might not be a 1:1 correspondence
    fig = pylab.figure()
    pylab.plot(x, y, '-o')

    foo = ParametricSpline(x,y)
    interp_d = S.linspace(0.0, 1.0, 500)
    interp_xy = foo(interp_d)
    pylab.plot(interp_xy[:,0], interp_xy[:,1])
    pylab.show()
