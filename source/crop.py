import fitz, sys

# name: (catalog page, x0, y0, x1, y1) as fractions of the page
CROPS = {
    "products/bopp-clear": (6, .06, .03, .96, .66),
    "products/bopp-brown": (19, 0.05, 0.255, 0.95, 0.76),
    "products/printed": (15, 0.03, 0.42, 0.97, 0.96),
    "products/duct": (21, 0.05, 0.22, 0.95, 0.71),
    "products/masking": (10, .04, .05, .96, .70),
    "products/pvc-pipe": (12, .04, .06, .96, .74),
    "products/electrical": (24, 0.02, 0.245, 0.98, 0.77),
    "products/aluminium": (14, 0.03, 0.37, 0.97, 0.6),
    "products/double-sided": (22, 0.36, 0.235, 0.98, 0.6),
    "products/cloth-colored": (36, 0.03, 0.2, 0.97, 0.74),
    "products/stretch-bubble": (35, 0.03, 0.225, 0.97, 0.645),
    "products/bag-seal": (30, 0.03, 0.235, 0.97, 0.76),
    "services/cartons": (40, 0.0, 0.62, 1.0, 1.0),
    "services/printing": (15, 0.03, 0.42, 0.97, 0.96),
    "services/sizes": (17, 0.03, 0.245, 0.97, 0.5),
    "services/solutions": (44, .0, .38, 1.0, .82),
    "hero": (44, .0, .38, 1.0, .95),
}

doc = fitz.open("catalog.pdf")
only = sys.argv[1:]
for name, (pg, x0, y0, x1, y1) in CROPS.items():
    if only and name not in only:
        continue
    page = doc[pg - 1]
    W, H = page.rect.width, page.rect.height
    clip = fitz.Rect(x0 * W, y0 * H, x1 * W, y1 * H)
    pix = page.get_pixmap(dpi=150 if name == "hero" else 115, clip=clip)
    pix.save(f"../assets/{name}.jpg", jpg_quality=82)
    print(name, pix.width, pix.height)
