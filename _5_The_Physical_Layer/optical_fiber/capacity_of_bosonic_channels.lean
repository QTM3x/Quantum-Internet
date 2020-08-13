import .capacity



/-
The two-way capacity of this lossy channel for any 
repeaterless implementation of the channel can be shown 
to be C = - log(1-η) per mode, where η represents the 
physical channel's transmissivity. η varies with distance 
exponentially with a constant loss (α) in dbm units.
-/
theorem two_way_capacity_Gaussian_channel : 
two_way_capacity Gaussian_channel = - real.log(1-η) :=
begin
    -- One of the main idea of the proof to establish 
    -- bounds is σ-stretching of the channel.
    sorry
end
