package NextflowExecutor


import (
	"context"
	"log"
	"nextflow-api-server/utils"
	"os"
	"os/exec"
	"path/filepath"
)

func ApplyBasicMethod(
	ctx context.Context,
	nextflowScript string,
	dockerImage string,
	logLocation string,
	objectID string,
	workPath string,
	inputPath string,
	outputPath string,
	additionalNextflowArgs *map[string]string,
	additionalScriptArgs *map[string]string) {
	if os.Getenv("NXF_EXECUTOR") != "local" {
		utils.ErrorLog.Printf("Nextflow Executor Not Supported Yet."); return
	}
	outputPathWithID := filepath.Join(outputPath, objectID)
	outputPathCurrent := filepath.Join(outputPath, "current/")
	workPathWithID := filepath.Join(workPath, objectID)
	pathCreateErr := os.MkdirAll(workPathWithID, os.ModePerm)
	if pathCreateErr != nil {
		utils.ErrorLog.Printf("Could not create 'work' directory: %s\n", pathCreateErr.Error())
		return
	}
	err := os.RemoveAll(outputPathCurrent+"/**")
	if err != nil {
		utils.ErrorLog.Printf("Error encountered deleting existing 'current' directory: %s\n", err.Error())
		return
	}
	// pathCreateErr = os.MkdirAll(outputPathCurrent, os.ModePerm)
	// if pathCreateErr != nil {
	// 	utils.ErrorLog.Panicf("Could not create 'current' Directory: %s\n", pathCreateErr.Error())
	// 	return
	// }
	pathCreateErr = os.MkdirAll(outputPathWithID, os.ModePerm)
	if pathCreateErr != nil {
		utils.ErrorLog.Printf("Could not create 'current' Directory: %s\n", pathCreateErr.Error())
		return
	}
	
	// var cmd *exec.Cmd = exec.Command("/bin/bash", "&& mkdir -p ", "/usr/bin/nextflow")
	var cmd *exec.Cmd = exec.Command("/bin/bash", "/usr/bin/nextflow")
	cmd.Dir = workPathWithID
	// cmd.Env = os.Environ()
	if len(logLocation) > 0 {
		// cmd.Args = append(cmd.Args, "-log", logLocation)
		cmd.Args = append(cmd.Args, "run")
		cmd.Args = append(cmd.Args, "-work-dir", workPathWithID)

	} else {
		// cmd.Args = append(cmd.Args, "-log", outputPathWithID)
		cmd.Args = append(cmd.Args, "run")
		cmd.Args = append(cmd.Args, "-work-dir", workPathWithID)
	}
	if additionalNextflowArgs != nil {
		for k, v := range *additionalNextflowArgs {
			cmd.Args = append(cmd.Args, k, v)
		}
	}
	cmd.Args = append(cmd.Args, nextflowScript, "--input_path", inputPath,
		"--output_path", outputPathWithID)

	if len(dockerImage) > 0 {
		cmd.Args = append(cmd.Args, "-with-docker", dockerImage)
	}

	if additionalScriptArgs != nil {
		for k, v := range *additionalScriptArgs {
			cmd.Args = append(cmd.Args, k, v)
		}
	}

	log.Println(cmd.Args)
	stdout, err := cmd.Output()
	if err != nil {
		utils.ErrorLog.Println(stdout)
		utils.ErrorLog.Println(err.Error())
	}

	err = os.Symlink(outputPathWithID, outputPathCurrent)
	if err != nil {
		utils.ErrorLog.Printf("Error encountered linking output directory to 'current' directory: %s\n", err.Error())
	}
	
	utils.InfoLog.Println(string(stdout))
}
