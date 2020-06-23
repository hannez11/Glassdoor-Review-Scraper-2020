import os

pages = [
('"https://www.glassdoor.com/Reviews/PolyOne-Reviews-E12620.htm"',"PolyOne"), ('"https://www.glassdoor.com/Reviews/Portland-General-Electric-Reviews-E541.htm"',"PortlandGeneralElectricCompany"), ('"https://www.glassdoor.com/Reviews/Potbelly-Sandwich-Works-Reviews-E29603.htm"',"Potbelly"), ('"https://www.glassdoor.com/Reviews/Power-Integrations-Reviews-E7206.htm"',"PowerIntegrations"), ('"https://www.glassdoor.com/Reviews/PPL-Reviews-E520.htm"',"PPL"), ('"https://www.glassdoor.com/Reviews/PQ-Reviews-E11358.htm"',"PQGroupHoldings"), ('"https://www.glassdoor.com/Reviews/PRA-Group-Reviews-E975783.htm"',"PRAGroup"), ('"https://www.glassdoor.com/Reviews/PRA-Health-Sciences-Reviews-E7380.htm"',"PRAHealthSciences"), ('"https://www.glassdoor.com/Reviews/Precigen-Reviews-E2445665.htm"',"Precigen"), ('"https://www.glassdoor.com/Reviews/Precision-BioSciences-Reviews-E2121249.htm"',"PrecisionBioSciences"), ('"https://www.glassdoor.com/Reviews/Preferred-Apartment-Communities-Reviews-E354632.htm"',"PreferredApartmentCommunities"), ('"https://www.glassdoor.com/Reviews/Preferred-Bank-Reviews-E38016.htm"',"PreferredBank"), ('"https://www.glassdoor.com/Reviews/Preformed-Line-Products-Reviews-E21452.htm"',"PreformedLineProductsCompany"), ('"https://www.glassdoor.com/Reviews/Premier-Reviews-E2076567.htm"',"Premier"), ('"https://www.glassdoor.com/Reviews/Premier-Financial-Bancorp-Reviews-E6051.htm"',"PremierFinancialBancorp"), ('"https://www.glassdoor.com/Reviews/Prestige-HealthCare-Resources-Reviews-E762364.htm"',"PrestigeConsumerHealthcare"), ('"https://www.glassdoor.com/Reviews/Prevail-Therapeutics-Reviews-E2207217.htm"',"PrevailTherapeutics"), ('"https://www.glassdoor.com/Reviews/PRGX-Global-Reviews-E6129.htm"',"PRGXGlobal"), ('"https://www.glassdoor.com/Reviews/PriceSmart-Reviews-E7189.htm"',"PriceSmart"), ('"https://www.glassdoor.com/Reviews/PrimeEnergy-Reviews-E5002.htm"',"PrimeEnergyResources"), ('"https://www.glassdoor.com/Reviews/Primerica-Reviews-E13616.htm"',"Primerica"), ('"https://www.glassdoor.com/Reviews/Primoris-Reviews-E229939.htm"',"PrimorisServices"), ('"https://www.glassdoor.com/Reviews/Principal-Financial-Group-Reviews-E2941.htm"',"PrincipalFinancialGroup"), ('"https://www.glassdoor.com/Reviews/Principia-Biopharma-Reviews-E2290243.htm"',"PrincipiaBiopharma"), ('"https://www.glassdoor.com/Reviews/Priority-Payment-Systems-Reviews-E405672.htm"',"PriorityTechnologyHoldings"), ('"https://www.glassdoor.com/Reviews/ProAssurance-Reviews-E1239.htm"',"ProAssurance"), ('""',"ProfessionalHoldingCorp."), ('"https://www.glassdoor.com/Reviews/Progenics-Pharmaceuticals-Reviews-E6461.htm"',"ProgenicsPharmaceuticals"), ('"https://www.glassdoor.com/Reviews/Progress-Reviews-E2083.htm"',"ProgressSoftware"), ('"https://www.glassdoor.com/Reviews/Progyny-Reviews-E1092741.htm"',"Progyny"), ('"https://www.glassdoor.com/Reviews/Prologis-Reviews-E2631.htm"',"Prologis"), ('"https://www.glassdoor.com/Reviews/Proofpoint-Reviews-E39140.htm"',"Proofpoint"), ('"https://www.glassdoor.com/Reviews/ProPetro-Services-Reviews-E710481.htm"',"ProPetroHoldingCorp."), ('"https://www.glassdoor.com/Reviews/PROS-Reviews-E41736.htm"',"PROSHoldings"), ('"https://www.glassdoor.com/Reviews/ProSight-Specialty-Insurance-Reviews-E1695.htm"',"ProSightGlobal"), ('"https://www.glassdoor.com/Reviews/Prosperity-Bank-Reviews-E112985.htm"',"ProsperityBancshares"), ('"https://www.glassdoor.com/Reviews/Protagonist-Therapeutics-Reviews-E1924707.htm"',"ProtagonistTherapeutics"), ('"https://www.glassdoor.com/Reviews/Protective-Insurance-Reviews-E1164.htm"',"ProtectiveInsurance"), ('"https://www.glassdoor.com/Reviews/Prothena-Reviews-E1036145.htm"',"Prothena"), ('"https://www.glassdoor.com/Reviews/Protolabs-Reviews-E388685.htm"',"ProtoLabs"),
]

left_pages = []
done = [filename.split(".")[0] for filename in os.listdir("C:\\Users\\hannez\\Desktop\\GD")]

for page in pages:
    firm = page[1]
    if firm not in done:
        left_pages.append(page)
    
print(left_pages)
print(len(left_pages))



#approach 2
# x = ['Penumbra', "People'sUnitedFinancial", 'PepsiCo', 'PerkinElmer', 'Personalis', 'PetMedExpress', 'Pfizer', 'PhathomPharmaceuticals', 'PhibroAnimalHealth', 'Phreesia', 'PhysiciansRealtyTrust', "Pilgrim'sPride", 'PinnacleFinancialPartners']
# y = ['PeoplesBancorp', 'PeoplesFinancialServicesCorp.', 'PerdoceoEducation', 'PerformanceFoodGroupCompany', 'Perspecta', 'PetIQ', 'PG&E', 'PhaseBioPharmaceuticals', 'PhilipMorrisInternational', 'Photronics', 'PICOHoldings', 'PierisPharmaceuticals', 'PinnacleWestCapital', 'PiperSandlerCompanies', 'Plantronics']
# z = ['PeoplesBancorpofNorthCarolina', "People'sUtahBancorp", 'Perficient', 'PerrigoCompany', 'PetIQ', 'Pfenex', 'PGTInnovations', 'PhibroAnimalHealth', 'Phillips66', 'Phunware', 'PiedmontOfficeRealtyTrust', 'PingIdentityHoldingCorp.', 'PioneerNaturalResourcesCompany', 'PJTPartners', 'PlayAGS', 'Pluralsight']

# copy = []
# print(len(copy), len(x), len(y), len(z))

# for i in pages:
#     # print(i)
#     # print(i[1])
#     # print(i[1] not in x)
#     if i[1] not in x and i[1] not in y and i[1] not in z:
#         print(i)
#         copy.append(i)
# print(len(copy))
# print(copy)
