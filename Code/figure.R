#!/usr/bin/env Rscript

# =========================================================
# Self-contained conceptual figure in R (no external data)
# =========================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(patchwork)
  library(scales)
  library(grid)
})

set.seed(42)

# ---------------------------------------------------------
# SECTION 1: Simulated geometry and inputs
# ---------------------------------------------------------

# Settlement boundary as polyline
boundary <- data.frame(
  x = c(1000, 2000, 3500, 4500),
  y = c(1000, 2500, 2000, 3000)
)

# Settlement area polygon
settlement_area <- data.frame(
  x = c(1000, 2000, 3500, 4500, 4500, 1000),
  y = c(1000, 2500, 2000, 3000, 1000, 1000)
)

# Main building centroid and background points
main_point <- data.frame(x = 2600, y = 2000)
background_pts <- data.frame(
  x = c(1500, 1800, 2200, 3000),
  y = c(1500, 1900, 1600, 2300)
)

# ---------------------------------------------------------
# SECTION 2: Point-to-line nearest distance (x)
# ---------------------------------------------------------

nearest_point_on_polyline <- function(px, py, line_df) {
  best <- list(dist2 = Inf, x = NA_real_, y = NA_real_)
  n <- nrow(line_df)

  for (i in 1:(n - 1)) {
    ax <- line_df$x[i];     ay <- line_df$y[i]
    bx <- line_df$x[i + 1]; by <- line_df$y[i + 1]
    abx <- bx - ax; aby <- by - ay
    apx <- px - ax; apy <- py - ay
    denom <- abx * abx + aby * aby

    if (denom == 0) next

    t <- (apx * abx + apy * aby) / denom
    t <- max(0, min(1, t))

    qx <- ax + t * abx
    qy <- ay + t * aby
    d2 <- (px - qx)^2 + (py - qy)^2

    if (d2 < best$dist2) {
      best$dist2 <- d2
      best$x <- qx
      best$y <- qy
    }
  }

  list(x = best$x, y = best$y, dist = sqrt(best$dist2))
}

np <- nearest_point_on_polyline(main_point$x, main_point$y, boundary)
measured_distance_x <- np$dist

cat(sprintf("Measured Distance (x) for main building: %.2f meters\n", measured_distance_x))

# ---------------------------------------------------------
# SECTION 3: Logistic saturation model f(x)
# ---------------------------------------------------------

L <- 1.0
k <- 0.005
x0 <- 300.0

logistic_saturation <- function(x, L, k, x0) {
  L / (1 + exp(-k * (x - x0)))
}

calculated_f_x <- logistic_saturation(measured_distance_x, L, k, x0)
cat(sprintf(
  "Calculated Cumulative Proportion (f(x)) for point at x=%.2f: %.4f\n",
  measured_distance_x, calculated_f_x
))

dist_grid <- seq(0, 1000, length.out = 200)
curve_df <- data.frame(
  x = dist_grid,
  fx = logistic_saturation(dist_grid, L, k, x0)
)

# ---------------------------------------------------------
# SECTION 4: Simulated map-like background texture + roads
# ---------------------------------------------------------

bbox <- list(xmin = 700, xmax = 4800, ymin = 700, ymax = 3300)

texture_df <- expand.grid(
  x = seq(bbox$xmin, bbox$xmax, length.out = 85),
  y = seq(bbox$ymin, bbox$ymax, length.out = 65)
) %>%
  mutate(intensity = pmax(0, pmin(1, rnorm(n(), mean = 0.6, sd = 0.12))))

roads <- bind_rows(
  data.frame(id = 1, x = c(850, 4680), y = c(1250, 1650)),
  data.frame(id = 2, x = c(1050, 4200), y = c(800, 3200)),
  data.frame(id = 3, x = c(1600, 4590), y = c(750, 2910))
)

measure_line <- data.frame(
  x = c(main_point$x, np$x),
  y = c(main_point$y, np$y)
)

# ---------------------------------------------------------
# SECTION 5: Left panel (map concept)
# ---------------------------------------------------------

p_map <- ggplot() +
  geom_tile(
    data = texture_df,
    aes(x = x, y = y, fill = intensity),
    alpha = 0.16,
    show.legend = FALSE
  ) +
  scale_fill_gradient(low = "white", high = "grey40") +
  geom_path(data = roads, aes(x = x, y = y, group = id), linewidth = 2.2, color = "#d9d9d9", alpha = 0.85) +
  geom_path(data = roads, aes(x = x, y = y, group = id), linewidth = 1.0, color = "white", alpha = 0.9) +
  geom_polygon(data = settlement_area, aes(x = x, y = y), fill = "#C1E1C1", alpha = 0.6, color = NA) +
  geom_path(data = boundary, aes(x = x, y = y), color = "black", linetype = "dashed", linewidth = 1.3) +
  geom_point(data = background_pts, aes(x = x, y = y), color = "gray40", alpha = 0.5, size = 2.5) +
  geom_point(data = main_point, aes(x = x, y = y), color = "red", shape = 4, stroke = 2.2, size = 7) +
  geom_path(data = measure_line, aes(x = x, y = y), color = "red", linetype = "dotted", linewidth = 1.1) +
  annotate(
    "label",
    x = (main_point$x + np$x) / 2 + 220,
    y = (main_point$y + np$y) / 2 + 110,
    label = sprintf("Measured\nDistance (x):\n%.1fm", measured_distance_x),
    fill = "white", color = "red", size = 3.8, fontface = "bold"
  ) +
  # Use cartesian coordinates (instead of fixed ratio) so both patchwork panels
  # occupy the same visual height in the final composed figure.
  coord_cartesian(xlim = c(bbox$xmin, bbox$xmax), ylim = c(bbox$ymin, bbox$ymax), expand = FALSE) +
  labs(
    title = "Step 1: Spatially Measure Point Distance to Boundary",
    subtitle = "All layers are simulated/generated in-script",
    x = NULL, y = NULL
  ) +
  theme_minimal(base_family = "sans", base_size = 12) +
  theme(
    panel.grid = element_blank(),
    axis.text = element_blank(),
    axis.ticks = element_blank(),
    aspect.ratio = 0.62,
    plot.title = element_text(size = 14, face = "bold"),
    plot.subtitle = element_text(size = 9.5, color = "gray30")
  )

# ---------------------------------------------------------
# SECTION 6: Right panel (logistic mapping)
# ---------------------------------------------------------

inflection_y <- logistic_saturation(x0, L, k, x0)

p_curve <- ggplot(curve_df, aes(x = x, y = fx)) +
  geom_line(color = "#1f77b4", linewidth = 1.3) +
  geom_hline(yintercept = L, color = "gray50", linetype = "dotted") +
  annotate("segment",
           x = measured_distance_x, xend = measured_distance_x, y = 0, yend = calculated_f_x,
           color = "red", linetype = "dotted", linewidth = 0.9) +
  annotate("segment",
           x = 0, xend = measured_distance_x, y = calculated_f_x, yend = calculated_f_x,
           color = "red", linetype = "dotted", linewidth = 0.9) +
  annotate("point", x = measured_distance_x, y = 0, color = "red", shape = 17, size = 3.2) +
  annotate("point", x = measured_distance_x, y = calculated_f_x, color = "red", size = 3.4) +
  annotate(
    "label",
    x = measured_distance_x + 120,
    y = calculated_f_x + 0.1,
    label = sprintf("Conceptual f(x):\n%.3f", calculated_f_x),
    fill = "white", color = "red", size = 3.8, fontface = "bold"
  ) +
  annotate(
    "text",
    x = 980, y = 1.02,
    label = sprintf("Upper Asymptote (L) = %.1f", L),
    hjust = 1, size = 3.5, color = "gray40"
  ) +
  scale_x_continuous(limits = c(0, 1000), expand = c(0, 0)) +
  scale_y_continuous(
    limits = c(0, 1.1),
    breaks = sort(unique(round(c(0, 0.2, 0.4, inflection_y, 0.8, 1.0), 3))),
    labels = label_number(accuracy = 0.1)
  ) +
  labs(
    title = "Step 2: Map Distance to Conceptual Saturation Model",
    x = "Distance from Settlement Boundary (x)",
    y = "Cumulative Proportion of Waste (f(x))"
  ) +
  theme_minimal(base_family = "sans", base_size = 12) +
  theme(
    aspect.ratio = 0.62,
    plot.title = element_text(size = 14, face = "bold"),
    panel.grid.minor = element_blank()
  )

# ---------------------------------------------------------
# SECTION 7: Compose and save
# ---------------------------------------------------------

final_plot <- p_map + p_curve +
  plot_layout(widths = c(1.3, 1)) +
  plot_annotation(title = "Fig 1: Methodological Framework for Spatially Modelling Waste Near Settlement Boundaries")

# Add a central mapping label to mimic conceptual linkage
final_plot <- final_plot +
  inset_element(
    ggplot() +
      annotate("label", x = 0.5, y = 0.5, label = "MAPPING\nCONCEPTUAL\nPOINT DISTANCE",
               size = 3.3, fontface = "bold", color = "#1f77b4", fill = alpha("white", 0.8)) +
      theme_void(),
    left = 0.46, right = 0.56, bottom = 0.43, top = 0.60
  )

print(final_plot)

# Optional save line:
# ggsave("methodological_framework_figure_R.png", final_plot, width = 14, height = 6.5, dpi = 300, bg = "white")
