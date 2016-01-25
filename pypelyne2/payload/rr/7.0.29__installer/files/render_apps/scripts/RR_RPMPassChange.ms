RPass_name=  "*Layer*"

if IsNetServer() then 
(
  RPass_nr =0
  for i= 1 to RPMdata.GetPassCount() do 
    (
    if (RPass_name==RPMdata.GetPassName(i))
    then RPass_nr=i 
    )
  if RPass_nr>0
    then RPMData.RMRestValues RPass_nr
    else quitMax #noPrompt
)

