using JuMP, Cbc

# Création du modèle avec le solveur Cbc
model = Model(Cbc.Optimizer)

# Nombre d'équipes et de journées
N = 36
T = 8

# Définition des variables
@variable(model, x[1:N, 1:N, 1:T], Bin)

# Variables supplémentaires pour contrôler les breaks
@variable(model, break_var[1:N, 2:6], Bin)


# Variables supplémentaires pour les matchs de chaque pot
@variable(model, two_matches_potA[1:T], Bin)
@variable(model, two_matches_potB[1:T], Bin)
@variable(model, two_matches_potC[1:T], Bin)
@variable(model, two_matches_potD[1:T], Bin)

# Variables supplémentaires pour les matchs entre chaque paire de pots
#=
@variable(model, three_matches_AB[1:T], Bin)
@variable(model, three_matches_AC[1:T], Bin)
@variable(model, three_matches_AD[1:T], Bin)
@variable(model, three_matches_BC[1:T], Bin)
@variable(model, three_matches_BD[1:T], Bin)
@variable(model, three_matches_CD[1:T], Bin)
=#


# Contrainte : une équipe ne peut pas jouer contre elle-même
@constraint(model, no_self_play[i in 1:N, t in 1:T], x[i, i, t] == 0)

# Contrainte : une équipe joue au plus 1 fois contre chaque autre équipe
@constraint(model, max_one_game[i in 1:N, j in 1:N; i != j], sum(x[i, j, t] + x[j, i, t] for t in 1:T) <= 1)

# Contrainte : chaque équipe joue exactement un match par journée
@constraint(model, one_game_per_day[t in 1:T, i in 1:N], sum(x[i, j, t] + x[j, i, t] for j in 1:N) == 1)

# Contraintes spécifiques pour chaque pot
for i in 1:N
    for pot_start in 1:9:28
        @constraint(model, sum(x[i, j, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
        @constraint(model, sum(x[j, i, t] for t in 1:T, j in pot_start:pot_start+8) == 1)
    end
end

# Contrainte pour l'alternance stricte au début et à la fin
@constraint(model, strict_alternate_start[i in 1:N], sum(x[i, j, 1] + x[i, j, 2] for j in 1:N) == 1)
@constraint(model, strict_alternate_end[i in 1:N], sum(x[i, j, 7] + x[i, j, 8] for j in 1:N) == 1)

# Contrainte pour limiter les breaks à 1 maximum
for i in 1:N
    for t in 2:6
        @constraint(model, sum(x[i, j, t] + x[i, j, t+1] for j in 1:N) <= 1 + break_var[i, t])
    end
    @constraint(model, sum(break_var[i, t] for t in 2:6) <= 1)
end

# Contraintes pour s'assurer qu'il y a exactement 1 jour avec 2 matchs pour chaque pot
@constraint(model, sum(two_matches_potA[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potB[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potC[t] for t in 1:T) == 1)
@constraint(model, sum(two_matches_potD[t] for t in 1:T) == 1)

# Contraintes pour s'assurer que chaque jour a soit 1 soit 2 matchs pour chaque pot
for t in 1:T
    @constraint(model, sum(x[i, j, t] for i in 1:9, j in 1:9) == 1 + two_matches_potA[t])
    @constraint(model, sum(x[i, j, t] for i in 10:18, j in 10:18) == 1 + two_matches_potB[t])
    @constraint(model, sum(x[i, j, t] for i in 19:27, j in 19:27) == 1 + two_matches_potC[t])
    @constraint(model, sum(x[i, j, t] for i in 28:36, j in 28:36) == 1 + two_matches_potD[t])
end

# Contraintes pour chaque paire de pots
#=
@constraint(model, sum(three_matches_AB[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_AC[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_AD[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_BC[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_BD[t] for t in 1:T) == 2)
@constraint(model, sum(three_matches_CD[t] for t in 1:T) == 2)


# Fonction pour définir la contrainte de matchs entre deux pots

function add_inter_pot_constraints(pot1_start, pot1_end, pot2_start, pot2_end, three_matches_var)
    for t in 1:T
        @constraint(model, sum(x[i, j, t] for i in pot1_start:pot1_end, j in pot2_start:pot2_end) + 
                            sum(x[i, j, t] for i in pot2_start:pot2_end, j in pot1_start:pot1_end) == 2 + three_matches_var[t])
    end
end


# Appliquer la contrainte pour chaque paire de pots
add_inter_pot_constraints(1, 9, 10, 18, three_matches_AB)
add_inter_pot_constraints(1, 9, 19, 27, three_matches_AC)
add_inter_pot_constraints(1, 9, 28, 36, three_matches_AD)
add_inter_pot_constraints(10, 18, 19, 27, three_matches_BC)
add_inter_pot_constraints(10, 18, 28, 36, three_matches_BD)
add_inter_pot_constraints(19, 27, 28, 36, three_matches_CD)
=#

# Fonction pour ajouter une contrainte de matchs maximum entre deux pots par journée
function add_max_inter_pot_constraint(pot1_start, pot1_end, pot2_start, pot2_end, min_matches, max_matches)
    for t in 1:T
        @constraint(model, min_matches <= sum(x[i, j, t] for i in pot1_start:pot1_end, j in pot2_start:pot2_end) + 
                            sum(x[i, j, t] for i in pot2_start:pot2_end, j in pot1_start:pot1_end) <= max_matches)
    end
end

# Appliquer la contrainte pour chaque paire de pots avec un maximum de 3 matchs par journée
add_max_inter_pot_constraint(1, 9, 10, 18, 2, 3) # Pots A et B
add_max_inter_pot_constraint(1, 9, 19, 27, 1, 3) # Pots A et C
add_max_inter_pot_constraint(1, 9, 28, 36, 1, 3) # Pots A et D
add_max_inter_pot_constraint(10, 18, 19, 27, 1, 3) # Pots B et C
add_max_inter_pot_constraint(10, 18, 28, 36, 1, 3) # Pots B et D
add_max_inter_pot_constraint(19, 27, 28, 36, 1, 3) # Pots C et D


# Lancement de l'optimisation pour trouver une solution réalisable
optimize!(model)


