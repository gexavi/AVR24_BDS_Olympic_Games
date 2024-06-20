import requests
import json

# URL de l'API WorldAthletics
url = 'https://lqf74cdt2jf7tktozacymhcvbe.appsync-api.eu-west-1.amazonaws.com/graphql'

# Headers de la requête avec JSON et la clé API du site WA
headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': 'da2-jgtxe5f2tvcafinp5zh5kmq5oq'
}

# Requête GraphQL
query = """
query GetCalendarCompetitionResults($competitionId: Int!, $day: Int, $eventId: Int!) {
  getCalendarCompetitionResults(competitionId: $competitionId, day: $day, eventId: $eventId) {
    competition {
      dateRange
      endDate
      name
      rankingCategory
      startDate
      venue
      __typename
    }
    eventTitles {
      rankingCategory
      eventTitle
      events {
        event
        eventId
        gender
        isRelay
        perResultWind
        withWind
        summary {
          competitor {
            teamMembers {
              id
              name
              iaafId
              urlSlug
              __typename
            }
            id
            name
            iaafId
            urlSlug
            birthDate
            __typename
          }
          mark
          nationality
          placeInRace
          placeInRound
          points
          raceNumber
          records
          wind
          __typename
        }
        races {
          date
          day
          race
          raceId
          raceNumber
          results {
            competitor {
              teamMembers {
                id
                name
                iaafId
                urlSlug
                __typename
              }
              id
              name
              iaafId
              urlSlug
              birthDate
              hasProfile
              __typename
            }
            mark
            nationality
            place
            points
            qualified
            records
            wind
            remark
            details {
              event
              eventId
              raceNumber
              mark
              wind
              placeInRound
              placeInRace
              points
              overallPoints
              placeInRoundByPoints
              overallPlaceByPoints
              __typename
            }
            __typename
          }
          startList {
            competitor {
              birthDate
              country
              id
              name
              urlSlug
              __typename
            }
            order
            pb
            sb
            bib
            __typename
          }
          wind
          __typename
        }
        __typename
      }
      __typename
    }
    options {
      days {
        date
        day
        __typename
      }
      events {
        gender
        id
        name
        combined
        __typename
      }
      __typename
    }
    parameters {
      competitionId
      day
      eventId
      __typename
    }
    __typename
  }
}
"""
list_competition_id = (7132391, 7093747, 6999193, 6977748, 6913163, 6951910, 6961749, 7138987, 7137279, 7125365, 7093740, 7078726, 7003368, 7003367, 6998524, 6903480, 6937596, 6930156, 6937294, 6939522, 6913256,
                       6997728, 6993598, 6987209, 6986221, 6988504)

list_epreuve_id = (10229630, 10229605, 10229631, 10229501, 10229502, 10229609, 10229610, 10229611, 10229612, 10229614, 10229615, 10229616, 10229617, 10229618, 10229619, 10229620, 10229621, 10229636,
                   10229634, 10229508, 10229628, 10229509, 10229510, 10229511, 10229512, 10229513, 10229514, 10229521, 10229522, 10229523, 10229524, 10229526, 10229527, 10229528, 10229529, 10229530,
                   10229531, 10229532, 10229533, 10229534, 10229535)

for compet in list_competition_id:
    for epr in list_epreuve_id:
        # Liste des paramètres de requête pour itération
        parametres_requete = [
            { "competitionId": compet,
            "day": None,
            "eventId": epr},
        
            # Ajoutez d'autres paramètres de requête au besoin
        ]

        # Itérer sur les paramètres de requête
        for parametre in parametres_requete:
            # Variables pour la requête GraphQL
            variables = {
                'competitionId': parametre["competitionId"],
                'day': parametre["day"],
                'eventId': parametre["eventId"]
            }

            # Payload de la requête avec la requête GraphQL et les variables
            payload = {
                'query': query,
                'variables': variables
            }

            # Envoyer la requête POST à l'API GraphQL
            response = requests.post(url, headers=headers, json=payload)

            # Vérifier si la requête a réussi (code d'état 200)
            if response.status_code == 200:
                # Récupérer les données de la réponse JSON
                data = response.json()
                # Traiter les données ici
                print(json.dumps(data, indent=2))  # Afficher les données formatées en JSON
                name_file = str(compet) + str(epr) + ".json"
                with open(name_file,"w") as fichier:
                    fichier.write(json.dumps(data, indent=2))
            else:
                print("Échec de la requête. Code d'état :", response.status_code)