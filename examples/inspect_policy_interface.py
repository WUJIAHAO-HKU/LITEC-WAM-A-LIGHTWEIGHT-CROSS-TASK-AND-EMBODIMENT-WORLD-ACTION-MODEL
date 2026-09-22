"""Print documented interfaces without loading a model or connecting hardware."""

from litec_wam_public.interface import SPECS

for name, spec in SPECS.items():
    latent = "base action space" if spec.latent_dimension is None else f"{spec.latent_dimension}-D latent"
    print(f"{name}: {spec.context_frames} context frames -> {spec.horizon} x {spec.dimension} actions; {latent}")

print("Interface documentation only; no learned policy is included.")
