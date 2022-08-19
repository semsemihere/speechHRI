def get_sequence_volume(frame=None):
    """source: https://github.com/snuq/VSEQF/blob/3ac717e1fa8c7371ec40503428bc2d0d004f0b35/vseqf.py#L142"""

    total = 0

    if bpy.context.scene.sequence_editor is None:
        return 0
    
    sequences = bpy.context.scene.sequence_editor.sequences_all
    depsgraph = bpy.context.evaluated_depsgraph_get()
    
    if frame is None:
          frame = bpy.context.scene.frame_current
          evaluate_volume = False
    else: evaluate_volume = True

    fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

    for sequence in sequences:

        if (sequence.type=="SOUND" and sequence.frame_final_start<frame and sequence.frame_final_end>frame and not sequence.mute):
           
            time_from = (frame - 1 - sequence.frame_start) / fps
            time_to = (frame - sequence.frame_start) / fps

            audio = sequence.sound.evaluated_get(depsgraph).factory

            chunk = audio.limit(time_from, time_to).data()
            #sometimes the chunks cannot be read properly, try to read 2 frames instead
            if (len(chunk)==0):
                time_from_temp = (frame - 2 - sequence.frame_start) / fps
                chunk = audio.limit(time_from_temp, time_to).data()
            #chunk still couldnt be read... just give up :\
            if (len(chunk)==0):
                average = 0

            else:
                cmax = abs(chunk.max())
                cmin = abs(chunk.min())
                if cmax > cmin:
                      average = cmax
                else: average = cmin

            if evaluate_volume:
                fcurve = fades.get_fade_curve(bpy.context, sequence, create=False)
                if fcurve:
                      volume = fcurve.evaluate(frame)
                else: volume = sequence.volume
            else:
                volume = sequence.volume

            total = total + (average * volume)
        
        continue 

    return total


volume = get_sequence_volume()
print(volume)