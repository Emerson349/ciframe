angular.module('deciframeApp').controller('SequenciaController', function($http, $window, ngProgressFactory, $anchorScroll, $location, GENEROS) {
  var vm = this;
  vm.sequenciasFamosas = [];
  vm.novaSequencia = "";
  vm.mensagemCadastro = "";
  vm.erroCadastro = false;
  vm.cadastrandoSequencia = false;
  vm.minhaSequencia = {};
  vm.isSearching = false;
  vm.showSearchResultsCount = false;
  vm.esfigeSpeech =  "";
  vm.musics = [];
  vm.generos = GENEROS;
  vm.meuGenero = "";
  vm.progressbar = ngProgressFactory.createInstance();

  vm.carregarSequencias = function() {
    $http.get("sequencias")
      .success(function(data) {
        vm.sequenciasFamosas = data.map(function(sequencia) {
          return {
            'id': sequencia.id,
            'acordes': sequencia.acordes.map(function(acorde) {
              return { 'acorde': acorde, 'cor': '#2E1C74' };
            })
          };
        });
      })
      .error(function() {
        vm.sequenciasFamosas = [];
        vm.mensagemCadastro = "Não foi possível carregar as sequências.";
        vm.erroCadastro = true;
      });
  };

  vm.cadastrarSequencia = function() {
    vm.mensagemCadastro = "";
    vm.erroCadastro = false;
    var acordes = vm.novaSequencia.split(",").map(function(acorde) {
      return acorde.trim();
    });
    vm.cadastrandoSequencia = true;
    $http.post("sequencias", { 'acordes': acordes })
      .success(function() {
        vm.cadastrandoSequencia = false;
        vm.erroCadastro = false;
        vm.mensagemCadastro = "Sequência cadastrada com sucesso!";
        vm.novaSequencia = "";
        vm.carregarSequencias();
      })
      .error(function(data, status) {
        vm.cadastrandoSequencia = false;
        vm.erroCadastro = true;
        if (data && data.erro) {
          vm.mensagemCadastro = data.erro;
        } else if (status === 409) {
          vm.mensagemCadastro = "Essa sequência já está cadastrada.";
        } else {
          vm.mensagemCadastro = "Sequência inválida. Use de 2 a 8 acordes separados por vírgula.";
        }
      });
  };

  vm.carregarSequencias();

  vm.temAcorde = function(acorde) {
    if (vm.minhaSequencia.acordes) {
      return (vm.minhaSequencia.acordes.indexOf(acorde) > -1);
    } else {
      return false;
    }
  }

  var createChordsString = function(chords) {
    var str = "";
    for (var i = 0; i < chords.length; i++) {
      str = str.concat(chords[i].acorde, ',');
    }
    return str.substring(0, str.length-1);
  }

  vm.pesquisarPorSequencia = function(sequencia) {
    if (sequencia) {
      vm.minhaSequencia = sequencia;
    }
    vm.progressbar.start();
    vm.esfigeSpeech = "Procurando músicas com base na sequencia...";
    vm.isSearching = true;
    vm.musics = [];

    var apiUrl = "";
    var searchString = "similares?sequencia=".concat(
      encodeURIComponent(createChordsString(vm.minhaSequencia.acordes)));
    if (vm.meuGenero !== "" && vm.meuGenero !== null) {
      searchString += "&generos="+vm.meuGenero;
    }
    $http.get(apiUrl.concat(searchString))
      .success(function(data) {
        vm.progressbar.complete();
        vm.esfigeSpeech = "Encontrei essas músicas";
        vm.isSearching = false;
        vm.showSearchResultsCount = true;
        vm.musics = data;
      })
      .error(function(data) {
        vm.esfigeSpeech = "Ops! Algo errado.";
        vm.isSearching = false;
        vm.showSearchResultsCount = false;
      });
  }

  vm.limparPesquisa = function() {
    vm.minhaSequencia = {};
    vm.musics = [];
  }

  vm.goToLirics = function(music) {
    $window.open(music.url);
  };

  vm.goToResults = function() {
    vm.showSearchResultsCount = false;
    $("body").animate({scrollTop: $("#results").offset().top}, "slow");
  };
});
