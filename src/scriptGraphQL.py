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

# Liste des paramètres de requête pour itération
parametres_requete = [
    { "competitionId": 7132391,
      "day": None,
      "eventId": 10229630},
  
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
    else:
        print("Échec de la requête. Code d'état :", response.status_code)
