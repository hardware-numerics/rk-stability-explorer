import argparse

from .utils import load_builtin
from .analysis import compute_results
from .rkplot_multiple import make_grid
from .rkplot_multiple import rkplot_multiple
from .utils import list_methods, list_methods_grouped   # 

import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        prog="rk-stability",
        description="Explore stability regions of Runge-Kutta methods",
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---- list ----
    subparsers.add_parser("list", help="List available methods")

    # ---- show ----
    show_parser = subparsers.add_parser("show", help="Show Butcher tableau")
    show_parser.add_argument("method")

    # ---- plot ----
    plot_parser = subparsers.add_parser("plot", help="Plot stability regions")
    plot_parser.add_argument("methods", nargs="+")
    plot_parser.add_argument("--n", type=int, default=200)
    plot_parser.add_argument("--cols", type=int, default=3)
    plot_parser.add_argument("--save", type=str, default=None)
    #plot_parser.add_argument("--hold", type=str, default=None)

    args = parser.parse_args()

    # ---- dispatch ----
    if args.command == "list":
        data = list_methods_grouped()
        max_len = max(len(group) for group in data)

        for group, methods in data.items():
            print(f"{group.ljust(max_len)} | {', '.join(methods)}")
        #for m in list_methods_grouped():
        #    print(m)
        

    elif args.command == "show":
        from .utils import print_butcher_table
        print_butcher_table(args.method)

    elif args.command == "plot":
        methods = args.methods

        X, Y = make_grid(n=args.n)
        Z = X + 1j * Y

        results = compute_results(methods, X, Y, Z)
        fig = rkplot_multiple(results, cols=args.cols)

        if args.save:
            fig.savefig(args.save, dpi=200, bbox_inches="tight")
            plt.show(block=False)
            plt.pause(1)
        else:    
        #if args.hold:
            plt.show()

    else:
        parser.print_help()

