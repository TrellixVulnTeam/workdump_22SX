print("### Initialize workspace and parameters ###")
rm(list=ls())
library("R.utils")
library("bnlearn")

print("### Script parameters ###")
preprocessing_directory = "./preprocessing_output/"
structures_directory = "./learned_structures/"
expected_file = "BN15a-B1_2.dsc"
score_based_algorithms = c("hc", "tabu")
scores = c("loglik", "aic", "bic", "bde", "bds", "bdj", "k2", "mbde", "bdla")
cv_folds = 10
cv_runs = 100

print("### Load files ###")
expected_network = bn.net(read.dsc(expected_file))
dataset_files = list.files(path=preprocessing_directory, full.names=TRUE)
dataset_files = dataset_files[grepl(".*dataset.*", dataset_files)]  # keep only files where "dataset" occurs in the filename
for (dataset_i in dataset_files) {
    #TODO remove: dataset_i = "./preprocessing_output/datasetNoMissing_threshold-0.5.csv"
    empirical_data = read.csv(dataset_i, check.names=FALSE, na.strings=c("NA","NaN", " ", ""))
    empirical_data[1] = NULL  # remove column 1 (ID column)
    dataset_name = basename(dataset_i)

    print("### Bypass sanitization ###")
    addLevels = function(col) {
        if(is.factor(col) && !("NotKnown" %in% levels(col))) return (factor(col, levels=c(levels(col), "NotKnown")))
        if(is.factor(col) && !("Known" %in% levels(col))) return (factor(col, levels=c(levels(col), "Known")))
        return (col)
    }
    empirical_data = as.data.frame(lapply(empirical_data, addLevels), check.names=FALSE)

    print("### Run parameter and structural learning ###")
    learned_networks = list()
    learned_networks[["expected"]] = bn.fit(expected_network, empirical_data)
    for (algorithm in score_based_algorithms) { for (score in scores) {
        algo_id = paste(algorithm, score, sep="_")
        print(paste("Running parameter learning with hyperparameters:", algo_id))
        learned_network = cextend(R.utils::doCall(structural.em, x=empirical_data, maximize=algorithm, score=score))
        learned_networks[[algo_id]] = bn.fit(learned_network, empirical_data)
    }}

    print("### Store learned output ###")
    for (network_name in names(learned_networks)) {
        network_dsc_file = paste(structures_directory, dataset_name, "-", network_name, ".dsc", sep="")
        write.dsc(network_dsc_file, learned_networks[[network_name]])
        print(paste("Saved network dsc to:", network_dsc_file))
        network_pdf_file = paste(structures_directory, dataset_name, "-", network_name, ".pdf", sep="")
        pdf(network_pdf_file)
        graphviz.plot(learned_networks[[network_name]])
        dev.off()
        print(paste("Saved network pdf to:", network_pdf_file))
    }

    print("### Generate statistics ###")
    complete_data = empirical_data[complete.cases(empirical_data), ]
    statistics_file = paste(structures_directory, dataset_name, "-", "statistics.csv", sep="")
    sink(statistics_file)
    writeLines(paste("network", "hammingDistance", "structuralHammingDistance", "meanError", sep=", "))
    for (network_name in names(learned_networks)) {
        learned_structure = bn.net(learned_networks[[network_name]])
        net_hamming = hamming(expected_network, learned_structure)
        net_shd = shd(expected_network, learned_structure)
        validation_runs = bn.cv(data=complete_data, bn=learned_structure, k=cv_folds, runs=cv_runs)
        mean_error = mean(sapply(validation_runs, function(obj) attr(obj, "mean")))
        writeLines(paste(network_name, net_hamming, net_shd, mean_error, sep=", "))
    }
    for (i in seq_len(sink.number())) print(sink(NULL))
    print(paste("Saved statistics to:", statistics_file))
}
# TODO: NA mean error threshold 1.0 statistics!
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="logl", k=2, runs=1), function(obj) attr(obj, "mean")))
#[1] NA
#There were 44 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="pred", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss.args(loss, bn, nodes, data, loss.args) : 
#  missing target node for which to compute the prediction error.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="pred-lw", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss.args(loss, bn, nodes, data, loss.args) : 
#  missing target node for which to compute the prediction error.
#In addition: There were 14 warnings (use warnings() to see them)

#### target: a character string, the label of target node for prediction in all loss functions but logl, logl-g and logl-cg.
#### dicrete + targetless -> logl

#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="logl-g", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'logl-g' may be used with continuous data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="cor", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'cor' may be used with continuous data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="cor-lw", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'cor-lw' may be used with continuous data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="mse", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'mse' may be used with continuous data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="mse-lw", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'mse-lw' may be used with continuous data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="logl-cg", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'logl-cg' may be used with a mixture of continuous and discrete data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="cor-lw-cg", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'cor-lw-cg' may be used with a mixture of continuous and discrete data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="mse-lw-cg", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'mse-lw-cg' may be used with a mixture of continuous and discrete data only.
#In addition: There were 14 warnings (use warnings() to see them)
#> mean(sapply(bn.cv(data=complete_data, bn=learned_structure, loss="pred-lw-cg", k=2, runs=1), function(obj) attr(obj, "mean")))
#Error in check.loss(loss, data, bn) : 
#  loss function 'pred-lw-cg' may be used with a mixture of continuous and discrete data only.
#In addition: There were 14 warnings (use warnings() to see them)
