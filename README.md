# ColorLCDVape-RE
 Reverse-engineering of some rechargeable disposable vapes that include a small color TFT LCD (Raz TN9000/Kraze HD7K/etc.).
 
 Further updates can be found at https://github.com/ginbot86/ColorLCDVape-RE

# Introduction
Some disposable vapes on the market include accoutrements like a color LCD screen and USB-C rechargeability, yet are single-use throwaway devices; this makes such devices quite ecologically harmful. On the other hand, this opens up opportunities for hardware salvage by hobbyists/engineers, reusing the vape as-is by refilling it with fresh vape juice and resetting the internal meter, or even customization by editing the onboard images.

While this project originally focused on one model (the Kraze HD7K, a.k.a. Raz TN9000), it has expanded to include other makes and models, including some with video game and Bluetooth/app connectivity. Check out the `docs` directory for detailed information on a specific model.

# Disclaimers/Hazards

Disposable vapes generally use Li-ion batteries without any protection circuitry. Short circuits could dissipate uncontrolled amounts of power, causing personal injury and/or property damage. Any work done on these vapes is done at your own risk.

It has been determined that there are multiple circuit revisions of these vapes, which may have incompatibilities that could result in device damage if versions are mismatched. Verify connections and firmware compatibility before proceeding with any modifications.

Additionally, vape juice/"e-liquid" can contain high concentrations of nicotine, which is absorbed through skin. Handling of the vape's internals should be done with gloves until the internal parts are cleaned of juice and/or residue.

# Additional Works

Other people's work on these vapes include, but are not limited to:

 - https://github.com/xbenkozx/RAZ-RE

Work done in the aforementioned repositories may or may not be based on work done in this project; it is meant to link similar projects in the hopes that more community efforts can be undertaken on these vapes.

# Models Documented
 - [Kraze HD7K / Raz TN9000](docs/KrazeHD7K-RazTN9000.md)