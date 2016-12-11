# ccmas-imgen

A system that utilizes computational creativity with multi-agent systems to 
generate imagery.

Multiple agents are generated at the beginning of the simulation, each with an
inspiring image source. At each step of the simulation, each agent generates a
potential brush stroke to be painted on a blank canvas, which is shared with all
agents. The potential brush strokes are evaluated based on novelty, value, and
surprisingness. The stroke with the highest evaluation score is selected. At the
end of the simulation, an image should be generated that is similar to the 
evaluation image, but unique in its own way.
