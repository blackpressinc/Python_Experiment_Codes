# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 16:59:28 2022

@author: blackpressinc
"""
# =============================================================================
# CoolProp is a project that provides the same functionality as REFPROP and also can
# be used as a wrapper for REFPROP in a number of computer languages.
# CoolProp should be useable even if you do not own or have REFPROP installed, it just
# uses it's own internal library for calculating properties instead of the NIST library
# More information can be found at http://www.coolprop.org/fluid_properties/index.html
# I have also tried PYroMat for people who do not have REFPROP but it doesn't calculate
# "extras" like viscosity, or thermal conductivity so I prefer to use REFPROP
# =============================================================================

import CoolProp.CoolProp as CP

# =============================================================================
# CoolProp documentation available at 
# https://buildmedia.readthedocs.org/media/pdf/coolprop/latest/coolprop.pdf
# =============================================================================

# =============================================================================
# CoolProp Example Calculations
# =============================================================================

# Define our STP values
Temperature = 300 # K
Pressure = 101350 # Pascals

Air_Viscosity = CP.PropsSI("viscosity","T",Temperature,"P",Pressure,"Air")
print("Reference STP Air Viscosity = 0.000019 Pa·s \nCalculated Air_Viscosity at STP = {:.4}".format(Air_Viscosity)+" Pa·s")

# =============================================================================
# For the units of a returned value check out the bottom of this page
# http://www.coolprop.org/coolprop/HighLevelAPI.html
# =============================================================================

# =============================================================================
# The following code demonstrates how to use REFPROP but I did have to copy the
# "REFPROP64.dll" into the folder which I can't  upload to GitHub so please copy
# your own file if you want to use REFPROP. (CoolProp seems to work just as well
# with it's own internal libraries)
# =============================================================================

HEOS = CP.PropsSI("T","P",Pressure,"Q",0,"HEOS::Water")
REFPROP = CP.PropsSI("T","P",Pressure,"Q",0,"REFPROP::Water")
print("Boiling point of water at STP calculated by HEOS (Open source) = {:.2f}".format(HEOS)+ " K")
print("Boiling point of water at STP calculated by REFPROP (Costs Money) = {:.2f}".format(REFPROP)+ " K")

# =============================================================================
# Now the following section loops uncertainties into property calculations by
# using the Uncertainties.py function wrapper. It can turn any function that
# returns a single scalar value into a function that accepts uncertainties by
# just calling the wrapper on an empty function definition.
# =============================================================================

# =============================================================================
# For more information on the uncertainties library check out
# https://pythonhosted.org/uncertainties/user_guide.html
# =============================================================================

from uncertainties import wrap # First we import the "wrap" function from uncertainties

# =============================================================================
# We wrap the CP.PropsSI we were using to get propertie data. Note that there are
# no paranthesis or function definitions inside the wrap command. In theory this
# should work on any function, even custom ones, as long as it returns a single number
# (might also work on numpy arrays or uncertainties.py's own unumpy arrays)
# =============================================================================

uProps = wrap(CP.PropsSI)

# =============================================================================
# Lets use the uncertainties ufloat variable type to add uncertainty to our STP
# values of temperature and pressure
# =============================================================================

from uncertainties import ufloat # Import the ufloat variable type from uncertainties

# =============================================================================
# The way to create a number with uncertainties is to use the ufloat function and then
# provide it with anominal value, uncertainty, and optionally a "tag" which we can use
# to track the contribution of Temperatures uncertainty in future calculations
# =============================================================================

uTemperature = ufloat(300, 10, "Temperature")
uPressure = ufloat(101350, 1000, "Pressure")

# =============================================================================
# Now we can simply call uProps the same way as we had previously called CP.PropsSI
# =============================================================================

uAir_Viscosity = uProps("viscosity","T",uTemperature,"P",uPressure,"Air")
print("Air Viscosity Calculated with Uncertainty = {:0.2u}".format(uAir_Viscosity)+ " Pa·s")

# =============================================================================
# Finally we can get the contribution of each component to the uncertainty of the
# Air Viscosity
# Note: If you are using Spyder IDE I just go into "Variable Explorer" and click on
# the "AffineScalarFunc" to see what data I can access for an uncertainty variable
# =============================================================================

for (var, error) in uAir_Viscosity.error_components().items():
    print("Contribution to Uncertainty from {} = +/- {:0.3}".format(var.tag, error))

# =============================================================================
# We can see that despite pressure varying but over 1,000 Pa, a 10 degree uncertainty in
# temperature had 3 orders of magnitude more effect on the uncertainty of viscosity
# =============================================================================
