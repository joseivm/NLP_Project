library(readr)

extract_value <- function(input_filename, output_filename){
  scanned_risk <- read_csv(input_filename, col_names = F)
  
  age <- unique(round(scanned_risk$X1))
  risk_1_year <- data.frame(age = age, risk = 0)
  
  scanned_risk$X1 <- as.numeric(format(round(scanned_risk$X1, 2), nsmall = 2))
  
  for (i in risk_1_year$age){
    for (j in 1:dim(scanned_risk)[1]){
      if (i > scanned_risk$X1[j]){
        next
      }
      else if (i == scanned_risk$X1[j]){
        risk_1_year$risk[risk_1_year$age == i] <- scanned_risk$X2[j]
        break
      }
       else {
         risk_1_year$risk[risk_1_year$age == i] <- (scanned_risk$X2[j] - scanned_risk$X2[j-1]) / 
           (scanned_risk$X1[j] - scanned_risk$X1[j-1]) * (i - scanned_risk$X1[j-1]) + 
           scanned_risk$X2[j-1]
         break
       }
    }
  }
  
  write_csv(risk_1_year, output_filename, col_names = T)
}