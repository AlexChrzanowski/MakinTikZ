import matplotlib.pyplot as plt
import makintikz

fig, ax = plt.subplots()

ax.errorbar(
    x=[1],
    y=[1],
    yerr=[0.5],
    label="data0",
)

ax.errorbar(
    x=[2],
    y=[2],
    yerr=[0.5],
    label="data1",
)

ax.legend()

print("\nCONTAINERS:")
for container in ax.containers:
    print(
        type(container),
        "container label:",
        container.get_label(),
        "main line label:",
        container.lines[0].get_label(),
    )

print("\nLEGEND HANDLES:")
for handle in ax.get_legend().legend_handles:
    print(type(handle), handle.get_label())

print("\nAXES LEGEND HANDLES/LABELS:")
handles, labels = ax.get_legend_handles_labels()
for handle, label in zip(handles, labels):
    print(type(handle), label)

code = makintikz.get_tikz_code(
    include_disclaimer=False,
)

print(code)

plt.show()